print("========== UNIT TESTING ==========\n")

import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.image_utils import load_image, prepare_image
from utils.translator import translate_from_english
from utils.pdf_generator import generate_pdf

from PIL import Image


# Test 1: Image Creation
print("Test 1: Image Creation")

try:
    image = Image.new("RGB", (100, 100))
    print("PASS: Image created successfully\n")
except Exception as e:
    print("FAIL:", e)


# Test 2: Translation Test
print("Test 2: Translation")

try:
    result = translate_from_english("Hello", "ta")
    print("PASS: Translation working:", result, "\n")
except Exception as e:
    print("FAIL:", e)


# Test 3: PDF Generation
print("Test 3: PDF Generation")

try:
    from PIL import Image

    # create dummy image
    test_image = Image.new("RGB", (200, 200), color="white")

    # create QA list (IMPORTANT: must be list of dict)
    qa_list = [
        {
            "question": "What is this?",
            "answer": "This is a test image"
        }
    ]

    heatmap_path = None
    language = "English"

    pdf_bytes, pdf_name = generate_pdf(
        image=test_image,
        qa_list=qa_list,
        heatmap_path=heatmap_path,
        language=language
    )

    print("PASS: PDF generated successfully")
    print("Generated file:", pdf_name, "\n")

except Exception as e:
    print("FAIL:", e)


print("========== UNIT TESTING COMPLETED ==========")
