import io
import cv2
import numpy as np
from PIL import Image, ImageOps

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



def _log_image(tag, arr):
    """Log basic image properties for debugging."""
    if arr is None:
        print(f"[CROP DEBUG] {tag}: None", flush=True)
        return
    if isinstance(arr, np.ndarray):
        ch = arr.shape[2] if len(arr.shape) == 3 else 1
        print(
            f"[CROP DEBUG] {tag}: shape={arr.shape} dtype={arr.dtype} "
            f"channels={ch} min={arr.min()} max={arr.max()} mean={arr.mean():.1f}",
            flush=True
        )
    elif isinstance(arr, io.BytesIO):
        arr.seek(0)
        data = arr.getvalue()
        arr.seek(0)
        print(f"[CROP DEBUG] {tag}: BytesIO len={len(data)}", flush=True)
    else:
        print(f"[CROP DEBUG] {tag}: type={type(arr).__name__}", flush=True)


def _decode_image(image):
    
    if isinstance(image, np.ndarray):
        return image

    if isinstance(image, io.BytesIO):
        data = image.getvalue()
    elif isinstance(image, (bytes, bytearray)):
        data = bytes(image)
    else:
        raise ValueError("Unsupported image type")

    if not data:
        raise ValueError("Empty image file")

    # Use PIL to decode (handles EXIF orientation via exif_transpose)
    with Image.open(io.BytesIO(data)) as source:
        source = ImageOps.exif_transpose(source)
        mode = source.mode
        if mode == "RGBA" or mode == "LA":
            # Composite transparent images onto white background
            white_bg = Image.new("RGBA", source.size, (255, 255, 255, 255))
            source = Image.alpha_composite(white_bg, source.convert("RGBA"))
        img_rgb = source.convert("RGB")

    img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)
    if img_bgr is None or img_bgr.size == 0:
        raise ValueError("Invalid image file")
    return img_bgr


def _clahe(gray):
    """Apply CLAHE contrast enhancement to a grayscale image."""
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def crop_id_photo(image, photo_type):
    """Detect a face in the image and crop it to the specified ID photo size."""
    if photo_type not in PHOTO_TYPES:
        raise ValueError(f"Invalid photo type: {photo_type}")

    config = PHOTO_TYPES[photo_type]
    crop_ratio = config["crop_ratio"]

    # Convert input to BGR array (handles EXIF orientation and alpha compositing)
    img_bgr = _decode_image(image)
    _log_image("input_decoded", img_bgr)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Build detection variants: grayscale, equalized, CLAHE
    detection_images = [
        gray,
        cv2.equalizeHist(gray),
        _clahe(gray),
    ]

    # Also try on alpha-channel ndarray inputs (transparency handled separately)
    if isinstance(image, np.ndarray) and len(image.shape) == 3 and image.shape[2] == 4:
        rgba = image
        rgb = cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGB)
        g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        detection_images.append(g)
        detection_images.append(cv2.equalizeHist(g))
        detection_images.append(_clahe(g))

    faces = []
    for idx, detection_image in enumerate(detection_images):
        detected = _detect_faces(detection_image)
        print(f"[CROP DEBUG] variant {idx}: {len(detected)} faces", flush=True)
        faces.extend(detected)

    faces = _merge_overlapping_boxes(faces)
    print(f"[CROP DEBUG] total unique faces after merge: {len(faces)}", flush=True)

    if len(faces) == 0:
        print(f"[CROP DEBUG] No face detected in any variant", flush=True)
        raise ValueError(
            "No face detected. Please upload a clearer photo where the face is "
            "fully visible (not covered by hair, hands, glasses glare, or shadows)."
        )

    # Use the biggest face
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, w, h = faces[0]
    print(f"[CROP DEBUG] selected face: x={x} y={y} w={w} h={h}", flush=True)

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
    top = center_y - int(crop_height * 0.43)

    right = left + crop_width
    bottom = top + crop_height

    # Handle out-of-bounds with white padding
    crop_top = max(0, top)
    crop_bottom = min(img_h, bottom)
    crop_left = max(0, left)
    crop_right = min(img_w, right)

    cropped_rgb = img_rgb[crop_top:crop_bottom, crop_left:crop_right]

    if cropped_rgb.size == 0:
        raise ValueError(
            f"Empty crop generated. Image size: {img_w}x{img_h}, "
            f"crop bounds: ({left}, {top}, {right}, {bottom})"
        )

    # Resize to exact print dimensions without stretching
    target_width = config["width"]
    target_height = config["height"]

    crop_h, crop_w = cropped_rgb.shape[:2]

    if crop_w == 0 or crop_h == 0:
        raise ValueError("Invalid crop dimensions")

    # Fit the cropped image inside the target dimensions
    scale = min(
        target_width / crop_w,
        target_height / crop_h
    )

    new_width = max(1, round(crop_w * scale))
    new_height = max(1, round(crop_h * scale))

    pil_cropped = Image.fromarray(cropped_rgb)
    resized = pil_cropped.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    # Add white padding to reach exact ID photo dimensions
    final_cropped = Image.new(
        "RGB",
        (target_width, target_height),
        (255, 255, 255)
    )

    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2

    final_cropped.paste(resized, (paste_x, paste_y))


    # Encode as PNG with print DPI
    output = io.BytesIO()
    final_cropped.save(output, format="PNG", dpi=(DPI, DPI))
    output.seek(0)

    return output