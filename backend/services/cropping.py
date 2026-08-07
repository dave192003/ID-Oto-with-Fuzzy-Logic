"""
ID photo cropping service.

Detects faces and crops images to standard ID photo dimensions.
"""

import io
import cv2
import numpy as np
from PIL import Image

# Print quality DPI
DPI = 300

# PHOTO CONFIGURATION (actual print size @300dpi)
PHOTO_TYPES = {
    "1x1": {
        "width": 300,
        "height": 300,
        "crop_ratio": 1.0
    },
    "1.5x1.5": {
        "width": 450,
        "height": 450,
        "crop_ratio": 1.0
    },
    "2x2": {
        "width": 600,
        "height": 600,
        "crop_ratio": 1.0
    },
    # 35mm x 45mm
    "passport": {
        "width": 413,
        "height": 531,
        "crop_ratio": 35 / 45
    }
}


def _to_rgb_array(image):
    """
    Convert an image (bytes, BytesIO, or numpy array) to an RGB numpy array.

    Args:
        image: Raw image bytes, BytesIO, or BGR/BGRA numpy array.

    Returns:
        numpy.ndarray: RGB image array.
    """
    if isinstance(image, np.ndarray):
        img_bgr = image
    elif isinstance(image, io.BytesIO):
        np_img = np.frombuffer(image.getvalue(), np.uint8)
        img_bgr = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)
    elif isinstance(image, (bytes, bytearray)):
        np_img = np.frombuffer(image, np.uint8)
        img_bgr = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)
    else:
        raise ValueError("Unsupported image type")

    if img_bgr is None:
        raise ValueError("Invalid image file")

    # Force RGB
    if len(img_bgr.shape) == 3 and img_bgr.shape[2] == 4:
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2RGB)
    else:
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def crop_id_photo(image, photo_type):
    """
    Detect a face in the image and crop it to the specified ID photo size.

    Args:
        image: Raw image bytes, BytesIO, or BGR/BGRA numpy array.
        photo_type (str): One of "1x1", "1.5x1.5", "2x2", "passport".

    Returns:
        io.BytesIO: In-memory PNG file of the cropped ID photo.

    Raises:
        ValueError: If the photo type is invalid or no face is detected.
    """
    if photo_type not in PHOTO_TYPES:
        raise ValueError(f"Invalid photo type: {photo_type}")

    config = PHOTO_TYPES[photo_type]
    crop_ratio = config["crop_ratio"]

    # Convert to RGB array
    img_rgb = _to_rgb_array(image)

    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Load face detection cascade
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier()

    if not face_cascade.load(cascade_path):
        print("WARNING: Unable to load CascadeClassifier! Retrying...")
        face_cascade = cv2.CascadeClassifier(cascade_path)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        raise ValueError("No face detected")

    # Use the biggest face
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, w, h = faces[0]

    img_h, img_w = img_rgb.shape[:2]

    # Calculate crop dimensions
    if crop_ratio == 1.0:
        crop_width = int(w * 2.3)
        crop_height = crop_width
    else:
        crop_height = int(h * 3.0)
        crop_width = int(crop_height * crop_ratio)

    # Center the crop on the face
    center_x = x + w // 2
    center_y = y + h // 2

    left = center_x - crop_width // 2
    top = center_y - int(crop_height * 0.40)

    right = left + crop_width
    bottom = top + crop_height

    # Handle out-of-bounds with white padding
    pad_left = max(0, -left)
    pad_top = max(0, -top)
    pad_right = max(0, right - img_w)
    pad_bottom = max(0, bottom - img_h)

    cropped_rgb = img_rgb[
        max(0, top):min(img_h, bottom),
        max(0, left):min(img_w, right)
    ]

    if pad_left > 0 or pad_top > 0 or pad_right > 0 or pad_bottom > 0:
        cropped_rgb = cv2.copyMakeBorder(
            cropped_rgb,
            pad_top,
            pad_bottom,
            pad_left,
            pad_right,
            borderType=cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )

    # Resize to the exact print dimensions
    pil_cropped = Image.fromarray(cropped_rgb)
    final_cropped = pil_cropped.resize(
        (config["width"], config["height"]),
        Image.Resampling.LANCZOS
    )

    # Encode as PNG with print DPI
    output = io.BytesIO()
    final_cropped.save(output, format="PNG", dpi=(DPI, DPI))
    output.seek(0)

    return output