import requests
from PIL import Image
from io import BytesIO


def load_image(upload_file=None, url=None):
    """
    Unified image loader:
    - Loads from file upload OR URL
    - Safe & error handled
    """

    try:
        # --------------------------
        # Upload File
        # --------------------------
        if upload_file is not None:
            img = Image.open(upload_file)
            return img.convert("RGB")

        # --------------------------
        # URL Image
        # --------------------------
        if url:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            return img.convert("RGB")

        raise ValueError("No image source provided")

    except Exception as e:
        raise ValueError(f"Image loading failed: {str(e)}")


def prepare_image(image, size=(512, 512)):
    """
    Resize image while preserving aspect ratio.
    Default resized to 512x512 (max size).
    """

    try:
        image = image.convert("RGB")

        # Preserve aspect ratio
        image.thumbnail(size, Image.Resampling.LANCZOS)

        return image

    except Exception as e:
        raise ValueError(f"Image preprocessing failed: {str(e)}")
