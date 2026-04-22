import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


import streamlit as st
from PIL import Image
from dotenv import load_dotenv # type: ignore
import os
import torch # type: ignore
import json
from pathlib import Path

# --------------------------------------------------
# ENV CONFIG
# --------------------------------------------------
os.environ["TORCH_LOGS"] = ""
os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"

load_dotenv()

DEVICE = "cpu"
MODEL_PATH = "model/trained_vqa"
DATASET_PATH = "data/my_vqa.json"

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

if "last_image_name" not in st.session_state:
    st.session_state.last_image_name = None

if "stop_voice" not in st.session_state:
    st.session_state.stop_voice = False

if "voice_buffer" not in st.session_state:
    st.session_state.voice_buffer = None

if "manual_question" not in st.session_state:
    st.session_state.manual_question = ""

if "dropdown_question" not in st.session_state:
    st.session_state.dropdown_question = "-- Select a Question --"

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------
if not os.path.exists(DATASET_PATH):
    st.error("Dataset file not found.")
    st.stop()

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    DATASET = json.load(f)

# --------------------------------------------------
# DATASET MATCH FUNCTION
# --------------------------------------------------
def get_answer_from_dataset(image_name, question):
    q = question.lower().strip()

    for item in DATASET:
        if item["image"] == image_name:
            all_questions = item.get("questions", []) + item.get("extra_questions", [])

            best_match = None
            max_match = 0

            for qa in all_questions:
                keywords = qa.get("question_keywords", [])
                match_count = sum(1 for k in keywords if k.lower() in q)

                if match_count > max_match:
                    max_match = match_count
                    best_match = qa

            if best_match and max_match > 0:
                return best_match["answer"]

    return None

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Visual Question Answering System", layout="wide")
st.title("🖼️ Visual Question Answering System")

# --------------------------------------------------
# IMPORT MODULES
# --------------------------------------------------
from model.gemini_api import get_answer_from_api
from utils.translator import translate_from_english
from utils.voice_utils import get_voice_input, speak_answer
from utils.pdf_generator import generate_pdf
from utils.image_utils import load_image, prepare_image
from model.gradcam import generate_gradcam
from transformers import ViltProcessor, ViltForQuestionAnswering # type: ignore

# --------------------------------------------------
# LOAD OFFLINE MODEL
# --------------------------------------------------
@st.cache_resource
def load_offline_model():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-mlm")
    model = ViltForQuestionAnswering.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )
    model.to(DEVICE)
    model.eval()
    return processor, model

processor, model = load_offline_model()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("⚙ Settings")

language_label = st.sidebar.selectbox(
    "🌍 Select Language",
    ["English", "Hindi", "Tamil", "Malayalam", "Telugu"]
)

model_choice = st.sidebar.selectbox(
    "🧠 Select Model",
    ["Offline Trained Model", "Gemini Vision"]
)

enable_gradcam = st.sidebar.checkbox("🔥 Enable Grad-CAM")
enable_voice = st.sidebar.checkbox("🎙 Enable Voice")
enable_pdf = st.sidebar.checkbox("📄 Enable PDF Report")

gemini_key = ""
if model_choice == "Gemini Vision":
    gemini_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")

# --------------------------------------------------
# IMAGE INPUT
# --------------------------------------------------
image_option = st.radio("Image Input Type", ["Upload Image", "Image URL"])
image = None
image_name = None

if image_option == "Upload Image":
    uploaded_file = st.file_uploader("📷 Upload image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = prepare_image(Image.open(uploaded_file))
        image_name = uploaded_file.name

        if image_name != st.session_state.last_image_name:
            st.session_state.qa_history = []
            st.session_state.manual_question = ""
            st.session_state.dropdown_question = "-- Select a Question --"
            st.session_state.last_image_name = image_name

else:
    url = st.text_input("🌐 Enter Image URL")
    if url:
        image = prepare_image(load_image(url=url))
        image_name = Path(url).name

        if image_name != st.session_state.last_image_name:
            st.session_state.qa_history = []
            st.session_state.manual_question = ""
            st.session_state.dropdown_question = "-- Select a Question --"
            st.session_state.last_image_name = image_name

# --------------------------------------------------
# APPLY VOICE BUFFER SAFELY
# --------------------------------------------------
if st.session_state.voice_buffer:
    st.session_state.manual_question = st.session_state.voice_buffer
    st.session_state.voice_buffer = None

# --------------------------------------------------
# QUESTION SECTION
# --------------------------------------------------
st.subheader("❓ Ask a Question (English Only)")

default_questions = [
    "How many people are in the picture?", 
    "Where are they?", 
    "Why are they there?", 
    "Who is with the children?", 
    "What is the weather like?", 
    "How many tents are visible in the picture?", 
    "What does the boy harvest?", 
    "What other vegetables can you find here?", 
    "What color do the houses have?", 
    "What tools can you see in the garden?"
]

st.selectbox(
    "Choose a default question:",
    ["-- Select a Question --"] + default_questions,
    key="dropdown_question"
)

st.text_input(
    "Or type your own question:",
    key="manual_question"
)

# --------------------------------------------------
# CLEAR BUTTONS
# --------------------------------------------------
col1, col2 = st.columns(2)

def clear_question():
    st.session_state.manual_question = ""

def clear_history():
    st.session_state.qa_history = []

with col1:
    st.button("🧹 Clear Question", on_click=clear_question)

with col2:
    st.button("🗑 Clear History", on_click=clear_history)

# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------
if enable_voice:
    if st.button("🎤 Voice Input (English)"):
        voice_text = get_voice_input("English")
        if voice_text:
            st.session_state.voice_buffer = voice_text
            st.rerun()

# --------------------------------------------------
# GET ANSWER
# --------------------------------------------------
if st.button("🚀 Get Answer"):

    if image is None:
        st.warning("Please upload an image.")
        st.stop()

    # Manual priority
    if st.session_state.manual_question.strip() != "":
        question = st.session_state.manual_question.strip()
    elif st.session_state.dropdown_question != "-- Select a Question --":
        question = st.session_state.dropdown_question
    else:
        st.warning("Please enter or select a question.")
        st.stop()

    with st.spinner("Answering..."):

        if model_choice == "Offline Trained Model":

            answer = get_answer_from_dataset(image_name, question)

            if not answer:
                encoding = processor(
                    images=image,
                    text=question,
                    return_tensors="pt"
                )
                encoding = {k: v.to(DEVICE) for k, v in encoding.items()}

                with torch.no_grad():
                    outputs = model(**encoding)

                predicted_idx = outputs.logits.argmax(-1).item()
                answer = model.config.id2label[predicted_idx]

        else:
            if not gemini_key:
                st.error("Please enter Gemini API Key")
                st.stop()

            answer = get_answer_from_api(image, question)

        # Translate answer
        if language_label != "English":
            answer = translate_from_english(answer, language_label)

        st.session_state.qa_history.append({
            "question": question,
            "answer": answer
        })

# --------------------------------------------------
# DISPLAY IMAGE
# --------------------------------------------------
if image is not None:
    st.image(image, caption="Input Image", width=400)


# --------------------------------------------------
# DISPLAY HISTORY
# --------------------------------------------------
if st.session_state.qa_history:

    st.markdown("## 📚 Question & Answer History")

    for idx, qa in enumerate(st.session_state.qa_history, 1):
        st.markdown(f"### {idx}. {qa['question']}")
        st.success(qa["answer"])

        if enable_voice and not st.session_state.stop_voice:
            speak_answer(qa["answer"], language_label)

# --------------------------------------------------
# STOP VOICE
# --------------------------------------------------
if enable_voice:
    if st.button("🔊 Stop Voice"):
        st.session_state.stop_voice = True

# --------------------------------------------------
# GRAD-CAM
# --------------------------------------------------
heatmap_path = None
if enable_gradcam and image is not None:
    heatmap_path = generate_gradcam(image)
    st.subheader("🔥 Grad-CAM")
    st.image(heatmap_path)

# --------------------------------------------------
# PDF GENERATION
# --------------------------------------------------
if enable_pdf and image is not None and st.session_state.qa_history:
     if st.button("📄 Generate PDF Report"):

        pdf_bytes, pdf_name = generate_pdf(
            image=image,
            qa_list=st.session_state.qa_history,
            heatmap_path=heatmap_path,
            language=language_label
        )

        st.download_button(
           "⬇ Download PDF Report",
            data=pdf_bytes,
            file_name=pdf_name,
            mime="application/pdf"
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown("👩‍💻 Developed by Jerlin Ishabel | Visual Question Answering System")
