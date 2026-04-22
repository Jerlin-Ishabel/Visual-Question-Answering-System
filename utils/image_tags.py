import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


def extract_tags(image: Image.Image):
    """
    Extracts simple visual attributes from image.
    Returns list of descriptive tags.
    """

    if cv2 is None:
        raise ImportError("OpenCV (cv2) is not installed.")

    try:
        img = np.array(image.convert("RGB"))

        # Safety check
        if img.size == 0:
            return ["Invalid image"]

        tags = []

        # ========================
        # Brightness
        # ========================
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        brightness = np.mean(gray)

        if brightness > 180:
            tags.append("Bright image")
        elif brightness < 80:
            tags.append("Dark image")
        else:
            tags.append("Normal brightness")

        # ========================
        # Contrast
        # ========================
        contrast = np.std(gray)

        if contrast < 40:
            tags.append("Low contrast")
        elif contrast < 80:
            tags.append("Medium contrast")
        else:
            tags.append("High contrast")

        # ========================
        # Dominant Color Detection
        # ========================
        avg_color = np.mean(img, axis=(0, 1))
        r, g, b = avg_color

        if r > g + 15 and r > b + 15:
            tags.append("Reddish tones")
        elif g > r + 15 and g > b + 15:
            tags.append("Greenish tones")
        elif b > r + 15 and b > g + 15:
            tags.append("Bluish tones")
        else:
            tags.append("Mixed colors")

        # ========================
        # Color Temperature
        # ========================
        if r > b:
            tags.append("Warm image")
        elif b > r:
            tags.append("Cool image")

        return tags

    except Exception as e:
        return [f"Tag extraction error: {str(e)}"]
