import os
from dotenv import load_dotenv # type: ignore
from PIL import Image
import google.generativeai as genai # type: ignore

# ================================
# LOAD API KEY
# ================================
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

model = None

if api_key:
    genai.configure(api_key=api_key)

    # ✅ Use model that your account supports
    model = genai.GenerativeModel("gemini-2.5-flash")


# ================================
# MAIN FUNCTION
# ================================
def get_answer_from_api(image: Image.Image, question: str) -> str:

    if model is None:
        return "Gemini API key not configured."

    try:
        response = model.generate_content(
            [question, image]
        )

        if response.text:
            return response.text.strip()
        else:
            return "No response from Gemini."

    except Exception as e:
        return f"Gemini API Error: {str(e)}"
