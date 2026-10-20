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
    """ Apply fuzzy-logic-based enhancement to an image."""

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

    # Apply enhancement
    enhanced = enhance_image(img, parameters)
    return enhanced



def enhance_image(img, parameters):
    """Enhance ID photos while preserving natural skin tones."""

    # 1. Limit denoising to preserve facial details.
    denoise_strength = float(
        np.clip(parameters["denoise"], 0.0, 2.0)
    )

    denoised = cv2.fastNlMeansDenoisingColored(
        img,
        None,
        denoise_strength,
        denoise_strength,
        7,
        21
    )

    # 2. Apply mild sharpening.
    sharpen_strength = float(
        np.clip(parameters["sharpen"], 0.0, 0.5)
    )

    blurred = cv2.GaussianBlur(
        denoised,
        (0, 0),
        1.0
    )

    sharpened = cv2.addWeighted(
        denoised,
        1.0 + sharpen_strength,
        blurred,
        -sharpen_strength,
        0
    )

    # 3. Keep brightness and contrast nearly neutral.
    alpha = float(
        np.clip(parameters["alpha"], 0.98, 2.03)
    )
    beta = float(
        np.clip(parameters["beta"], -2.0, 3.0)
    )

    enhanced = cv2.convertScaleAbs(
        sharpened,
        alpha=alpha,
        beta=beta
    )

    return enhanced



def encode_image_png(img_bgr):
    """ Encode a BGR image array as a PNG file. """
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    output = io.BytesIO()

    pil_img.save(
        output,
        format="PNG",
        dpi=(DPI, DPI)
    )
    output.seek(0)
    return output