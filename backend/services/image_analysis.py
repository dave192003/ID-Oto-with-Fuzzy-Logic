"""
Image analysis service.

Extracts quantitative features from images that are used
as inputs to the fuzzy inference system.
"""

import io
import cv2
import numpy as np


def _to_numpy_array(image):
    """
    Convert an image (bytes, BytesIO, or numpy array) to a BGR numpy array.

    Args:
        image: Raw image bytes, BytesIO, or numpy array.

    Returns:
        numpy.ndarray: BGR image array.
    """
    if isinstance(image, np.ndarray):
        return image

    if isinstance(image, io.BytesIO):
        image = image.getvalue()

    if isinstance(image, (bytes, bytearray)):
        np_img = np.frombuffer(image, np.uint8)
        return cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    raise ValueError("Unsupported image type")


def get_brightness(img):
    """
    Calculate the average brightness of an image.

    Args:
        img (numpy.ndarray): BGR image array.

    Returns:
        float: Mean pixel intensity (0-255).
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return round(float(np.mean(gray)), 2)


def get_contrast(img):
    """
    Calculate the contrast of an image using standard deviation.

    Args:
        img (numpy.ndarray): BGR image array.

    Returns:
        float: Standard deviation of pixel intensities.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return round(float(gray.std()), 2)


def get_sharpness(img):
    """
    Calculate the sharpness of an image using Laplacian variance.

    Args:
        img (numpy.ndarray): BGR image array.

    Returns:
        float: Variance of the Laplacian (higher = sharper).
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2)


def get_noise(img):
    """
    Estimate the noise level of an image.

    Compares the image to a Gaussian-blurred version and
    measures the mean absolute difference.

    Args:
        img (numpy.ndarray): BGR image array.

    Returns:
        float: Mean absolute difference (higher = noisier).
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    return round(float(np.mean(cv2.absdiff(gray, blur))), 2)


def analyze_image(image):
    """
    Extract all image features used by the fuzzy inference system.

    Accepts bytes, BytesIO, or numpy array.

    Args:
        image: Raw image bytes, BytesIO, or BGR numpy array.

    Returns:
        dict: {
            "brightness": float,
            "contrast": float,
            "sharpness": float,
            "noise": float
        }
    """
    img = _to_numpy_array(image)

    return {
        "brightness": get_brightness(img),
        "contrast": get_contrast(img),
        "sharpness": get_sharpness(img),
        "noise": get_noise(img)
    }