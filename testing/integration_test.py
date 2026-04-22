print("========== INTEGRATION TESTING ==========\n")

import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.image_utils import prepare_image
from utils.translator import translate_from_english
from utils.pdf_generator import generate_pdf

from PIL import Image


# Test 1: Image + Preprocessing Integration
print("Test 1: Image Loading + Preprocessing Integration")

try:
    test_image = Image.new("RGB", (224, 224), color="blue")

    processed_image = prepare_image(test_image)

    print("PASS: Image preprocessing integration successful\n")

except Exception as e:
    print("FAIL:", e)


# Test 2: Translation + PDF Integration (FIXED)
print("Test 2: Translation + PDF Generation Integration")

try:
    # create image
    test_image = Image.new("RGB", (200, 200), color="white")

    question = "What is shown in the image?"
    answer = "This is a test image"

    # translate
    translated_answer = translate_from_english(answer, "Tamil")

    # create QA list
    qa_list = [
        {
            "question": question,
            "answer": translated_answer
        }
    ]

    heatmap_path = None
    language = "Tamil"

    pdf_bytes, pdf_name = generate_pdf(
        image=test_image,
        qa_list=qa_list,
        heatmap_path=heatmap_path,
        language=language
    )

    print("PASS: Translation and PDF integration successful\n")

except Exception as e:
    print("FAIL:", e)


# Test 3: Full Pipeline Integration Simulation (FIXED)
print("Test 3: Full Module Integration Simulation")

try:
    image = Image.new("RGB", (224, 224), color="green")

    processed = prepare_image(image)

    question = "What is this?"
    answer = "Sample answer"

    translated = translate_from_english(answer, "Tamil")

    qa_list = [
        {
            "question": question,
            "answer": translated
        }
    ]

    pdf_bytes, pdf_name = generate_pdf(
        image=image,
        qa_list=qa_list,
        heatmap_path=None,
        language="Tamil"
    )

    print("PASS: Full system integration successful\n")

except Exception as e:
    print("FAIL:", e)


print("========== INTEGRATION TESTING COMPLETED ==========")
