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


# Haar cascade classifiers used for face detection. Several cascades are tried
# because detection quality varies between images and OpenCV builds.
CASCADE_FILES = [
    "haarcascade_frontalface_default.xml",
    "haarcascade_frontalface_alt2.xml",
    "haarcascade_frontalface_alt.xml",
    "haarcascade_frontalface_alt_tree.xml",
]

# Detection parameter sets, ordered from strict to relaxed. Trying multiple
# parameter sets makes face detection robust to different image sizes, poses,
# and image-quality issues introduced by enhancement/background removal.
DETECTION_PARAM_SETS = [
    {"scaleFactor": 1.05, "minNeighbors": 6, "minSize": (35, 35), "flags": cv2.CASCADE_SCALE_IMAGE},
    {"scaleFactor": 1.10, "minNeighbors": 5, "minSize": (30, 30), "flags": cv2.CASCADE_SCALE_IMAGE},
    {"scaleFactor": 1.15, "minNeighbors": 4, "minSize": (25, 25), "flags": cv2.CASCADE_SCALE_IMAGE},
    {"scaleFactor": 1.20, "minNeighbors": 3, "minSize": (20, 20), "flags": cv2.CASCADE_SCALE_IMAGE},
]

# Upscale images smaller than this width before detection so the Haar cascade
# has enough resolution to find the face.
_MIN_DETECTION_WIDTH = 900


def _load_cascades():
    """Load every available Haar cascade classifier."""
    cascades = []
    for name in CASCADE_FILES:
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + name)
        if not cascade.empty():
            cascades.append(cascade)
    return cascades


_CASCADES = _load_cascades()


def _resize_for_detection(img, min_width=_MIN_DETECTION_WIDTH):
    """Upscale small images so faces are large enough for the Haar cascade."""
    h, w = img.shape[:2]
    if w >= min_width:
        return img, 1.0
    scale = min_width / float(w)
    new_size = (min_width, max(1, int(h * scale)))
    return cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC), scale


def _detect_faces(gray):
    """Detect faces using multiple cascades and parameter sets."""
    gray_work, scale = _resize_for_detection(gray)
    variants = [gray_work, cv2.equalizeHist(gray_work)]

    found = []
    for variant in variants:
        for cascade in _CASCADES:
            for params in DETECTION_PARAM_SETS:
                try:
                    faces = cascade.detectMultiScale(
                        variant,
                        scaleFactor=params["scaleFactor"],
                        minNeighbors=params["minNeighbors"],
                        minSize=params["minSize"],
                        flags=params["flags"],
                    )
                except cv2.error:
                    continue
                if len(faces) == 0:
                    continue
                faces = np.asarray(faces, dtype=np.float32)
                if scale != 1.0:
                    faces = faces / scale
                for (x, y, w, h) in faces:
                    found.append((int(x), int(y), int(w), int(h)))
    return found


def _merge_overlapping_boxes(boxes):
    """Drop duplicate detections that mostly overlap a larger box."""
    if not boxes:
        return []
    boxes = sorted(boxes, key=lambda b: b[2] * b[3], reverse=True)
    kept = []
    for box in boxes:
        x, y, w, h = box
        duplicate = False
        for (kx, ky, kw, kh) in kept:
            inter_x = max(0, min(x + w, kx + kw) - max(x, kx))
            inter_y = max(0, min(y + h, ky + kh) - max(y, ky))
            inter = inter_x * inter_y
            if inter == 0:
                continue
            smaller_area = min(w * h, kw * kh)
            if smaller_area > 0 and inter / smaller_area > 0.5:
                duplicate = True
                break
        if not duplicate:
            kept.append(box)
    return kept


def _to_rgb_array(image):
   
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
    """Detect a face in the image and crop it to the specified ID photo size."""
    if photo_type not in PHOTO_TYPES:
        raise ValueError(f"Invalid photo type: {photo_type}")

    config = PHOTO_TYPES[photo_type]
    crop_ratio = config["crop_ratio"]

    # Convert to RGB array
    img_rgb = _to_rgb_array(image)

    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Detect faces using several cascades and parameter sets for robustness.
    faces = _merge_overlapping_boxes(_detect_faces(gray))

    if len(faces) == 0:
        raise ValueError(
            "No face detected. Please upload a clearer photo where the face is "
            "fully visible (not covered by hair, hands, glasses glare, or shadows)."
        )

    # Use the biggest face
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, w, h = faces[0]

    img_h, img_w = img_rgb.shape[:2]

    # Calculate crop dimensionss
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
    top = center_y - int(crop_height * 0.43)

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