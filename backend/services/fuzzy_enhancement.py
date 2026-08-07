"""
Fuzzy enhancement service.

Applies the Mamdani Fuzzy Inference System to enhance images.
Uses the existing fuzzy logic implementation from the fuzzy_logic package.
"""

import io
import cv2
import numpy as np
from PIL import Image

from fuzzy_logic.inference import fuzzy_logic
from services.image_analysis import _to_numpy_array

# Print quality DPI
DPI = 300


def apply_fuzzy_enhancement(image, features=None):
    """
    Apply fuzzy-logic-based enhancement to an image.

    Args:
        image: Raw image bytes, BytesIO, or BGR numpy array.
        features (dict, optional): Pre-computed image features.
            If None, features will be computed from the image.

    Returns:
        numpy.ndarray: Enhanced BGR image array.
    """
    print("===== FUZZY ENHANCEMENT =====", flush=True)

    # Convert to numpy array
    img = _to_numpy_array(image)
    print("Input shape:", img.shape, flush=True)
    print("Input dtype:", img.dtype, flush=True)

    # Compute features if not provided
    if features is None:
        from services.image_analysis import analyze_image
        features = analyze_image(img)

    print("Features:", features, flush=True)

    # Run fuzzy logic pipeline
    decision = fuzzy_logic(features)
    parameters = decision["parameters"]
    print("===== DECISION =====", flush=True)
    print(parameters, flush=True)

    # Apply enhancement
    enhanced = enhance_image(img, parameters)

    print("Output shape:", enhanced.shape, flush=True)
    print("Min:", enhanced.min(), flush=True)
    print("Max:", enhanced.max(), flush=True)

    return enhanced


def enhance_image(img, parameters):
    """
    Apply enhancement operations to an image based on fuzzy parameters.

    Args:
        img (numpy.ndarray): BGR image array.
        parameters (dict): Enhancement parameters with keys:
            alpha, beta, sharpen, denoise

    Returns:
        numpy.ndarray: Enhanced BGR image array.
    """
    print("===== ENHANCE DEBUG =====", flush=True)
    print("Parameters:", parameters, flush=True)

    denoised = cv2.fastNlMeansDenoisingColored(
        img,
        None,
        parameters["denoise"],
        parameters["denoise"],
        7,
        21
    )

    # Use stable sharpening kernel
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)

    sharpened = cv2.filter2D(
        denoised,
        -1,
        kernel
    )

    enhanced = cv2.convertScaleAbs(
        sharpened,
        alpha=float(parameters["alpha"]),
        beta=float(parameters["beta"])
    )

    return enhanced


def encode_image_png(img_bgr):
    """
    Encode a BGR image array as a PNG file.

    Args:
        img_bgr (numpy.ndarray): BGR image array.

    Returns:
        io.BytesIO: In-memory PNG file.
    """
    print("===== ENCODE PNG =====", flush=True)
    print("Shape:", img_bgr.shape, flush=True)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(img_rgb)

    output = io.BytesIO()

    pil_img.save(
        output,
        format="PNG",
        dpi=(DPI, DPI)
    )

    output.seek(0)

    print("PNG SIZE:", len(output.getvalue()), flush=True)

    return output