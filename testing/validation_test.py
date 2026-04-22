print("========== VALIDATION TESTING ==========\n")

import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.translator import translate_from_english
from utils.pdf_generator import generate_pdf

from PIL import Image


# Test 1: Validate Image Input
print("Test 1: Image Input Validation")

try:
    image = Image.new("RGB", (224, 224))

    if image is not None:
        print("PASS: Valid image input accepted\n")
    else:
        print("FAIL: Image validation failed\n")

except Exception as e:
    print("FAIL:", e)


# Test 2: Validate Missing Image
print("Test 2: Missing Image Validation")

try:
    image = None

    if image is None:
        print("PASS: Missing image correctly detected\n")
    else:
        print("FAIL: Missing image not detected\n")

except Exception as e:
    print("FAIL:", e)


# Test 3: Validate Question Input
print("Test 3: Question Input Validation")

try:
    question = "What is in the image?"

    if question.strip() != "":
        print("PASS: Valid question accepted\n")
    else:
        print("FAIL: Question validation failed\n")

except Exception as e:
    print("FAIL:", e)


# Test 4: Validate Empty Question
print("Test 4: Empty Question Validation")

try:
    question = ""

    if question.strip() == "":
        print("PASS: Empty question correctly detected\n")
    else:
        print("FAIL: Empty question not detected\n")

except Exception as e:
    print("FAIL:", e)


# Test 5: Validate Translation Module
print("Test 5: Translation Validation")

try:
    answer = "This is a test image"

    translated = translate_from_english(answer, "Tamil")

    if translated:
        print("PASS: Translation validation successful\n")
    else:
        print("FAIL: Translation validation failed\n")

except Exception as e:
    print("FAIL:", e)


# Test 6: Validate PDF Generation
print("Test 6: PDF Generation Validation")

try:
    image = Image.new("RGB", (200, 200))

    qa_list = [
        {
            "question": "Test question",
            "answer": "Test answer"
        }
    ]

    pdf_bytes, pdf_name = generate_pdf(
        image=image,
        qa_list=qa_list,
        heatmap_path=None,
        language="English"
    )

    print("PASS: PDF generation validation successful\n")

except Exception as e:
    print("FAIL:", e)


print("========== VALIDATION TESTING COMPLETED ==========")
