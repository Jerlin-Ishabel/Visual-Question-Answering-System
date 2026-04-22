# model/gradcam.py

import os
import uuid
import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None

# ================================
# OUTPUT FOLDER (RELATIVE PATH)
# ================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "gradcam")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ================================
# GENERATE HEATMAP
# ================================
def generate_gradcam(image: Image.Image) -> str:
    """
    Lightweight pseudo-GradCAM using edge intensity.
    Returns saved heatmap image path.
    """

    if cv2 is None:
        raise ImportError("OpenCV (cv2) is not installed.")

    try:
        # Convert PIL → numpy RGB
        img = np.array(image.convert("RGB"))

        # Resize if too small
        if img.shape[0] < 100 or img.shape[1] < 100:
            img = cv2.resize(img, (300, 300))

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 80, 200)

        # Normalize
        edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX)

        # Create heatmap
        heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)

        # Overlay
        overlay = cv2.addWeighted(img, 0.65, heatmap, 0.35, 0)

        # Save image
        filename = f"gradcam_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(OUTPUT_DIR, filename)

        Image.fromarray(overlay).save(output_path)

        return output_path

    except Exception as e:
        raise RuntimeError(f"GradCAM generation failed: {str(e)}")
