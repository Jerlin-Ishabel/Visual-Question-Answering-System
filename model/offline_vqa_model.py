import torch # type: ignore
from PIL import Image
from transformers import ViltProcessor, ViltForQuestionAnswering # type: ignore

MODEL_PATH = "model/trained_vqa"
DEVICE = "cpu"

# =========================
# LOAD MODEL (SAFE)
# =========================
def load_model():
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-mlm")

    model = ViltForQuestionAnswering.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )

    model.to(DEVICE)
    model.eval()

    return processor, model


processor, model = load_model()


# =========================
# OFFLINE ANSWER FUNCTION
# =========================
def get_offline_answer(image: Image.Image, question: str):

    try:
        # Ensure RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Encoding
        encoding = processor(
            images=image,
            text=question,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        encoding = {k: v.to(DEVICE) for k, v in encoding.items()}

        with torch.no_grad():
            outputs = model(**encoding)

        # Get probabilities
        probs = torch.softmax(outputs.logits, dim=-1)

        confidence, predicted_idx = torch.max(probs, dim=-1)

        predicted_idx = predicted_idx.item()
        confidence = confidence.item()

        answer = model.config.id2label[predicted_idx]

        return answer, confidence

    except Exception as e:
        return f"Error: {str(e)}", 0.0
