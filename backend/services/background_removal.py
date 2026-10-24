
import io
import cv2
import numpy as np
import time
from rembg import remove, new_session
from PIL import Image, ImageOps

DPI = 300
MAX_SIZE = 384

# Load BiRefNet Portrait once when the backend starts
BG_SESSION_HQ = new_session("birefnet-portrait")
BG_SESSION_FAST = new_session("u2netp")


def _log_image(tag, arr):
    """Log basic image properties for debugging."""
    if isinstance(arr, np.ndarray):
        ch = arr.shape[2] if len(arr.shape) == 3 else 1
        print(
            f"[BG DEBUG] {tag}: shape={arr.shape} dtype={arr.dtype} "
            f"channels={ch} min={arr.min()} max={arr.max()} mean={arr.mean():.1f}",
            flush=True
        )
    elif isinstance(arr, io.BytesIO):
        arr.seek(0)
        data = arr.getvalue()
        arr.seek(0)
        print(f"[BG DEBUG] {tag}: BytesIO len={len(data)}", flush=True)
    else:
        print(f"[BG DEBUG] {tag}: type={type(arr).__name__}", flush=True)


def _to_bytes(image):
    """Convert an image (bytes, BytesIO, or numpy array) to raw bytes."""
    if isinstance(image, (bytes, bytearray)):
        return bytes(image)

    if isinstance(image, io.BytesIO):
        return image.getvalue()

    if isinstance(image, np.ndarray):
        success, encoded = cv2.imencode(".jpg", image)
        if not success:
            raise ValueError("Failed to encode image")
        return encoded.tobytes()

    raise ValueError("Unsupported image type")


def refine_edges(img, erode_size=2, blur_size=3):
    """Refine the alpha edges of an RGBA image."""
    img = img.convert("RGBA")
    rgba = np.array(img)

    alpha = rgba[:, :, 3]

    if erode_size > 0:
        kernel_size = erode_size * 2 + 1
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        alpha = cv2.erode(alpha, kernel, iterations=1)

    if blur_size > 1:
        if blur_size % 2 == 0:
            blur_size += 1

        alpha = cv2.GaussianBlur(
            alpha,
            (blur_size, blur_size),
            0
        )

    rgba[:, :, 3] = alpha

    return Image.fromarray(rgba)



def remove_background(image, mode = "fast"):
    """Remove background using BiRefNet with reduced memory usage.

    Modes:
      - "fast"        : lightweight u2netp model (quick, lower detail)
      - "high" / "high-quality" : heavier birefnet-portrait model (slower, higher detail)
    """
    t0 = time.time()

    if mode == "fast":
        session = BG_SESSION_FAST
    elif mode in ("high", "high-quality"):
        session = BG_SESSION_HQ
    else:
        raise ValueError(f"Invalid background removal mode: {mode}")
    
    _log_image("input", image)
    image_bytes = _to_bytes(image)

    with Image.open(io.BytesIO(image_bytes)) as source:
        original = ImageOps.exif_transpose(source).convert("RGB")

    original_size = original.size
    _log_image("original_decoded", np.array(original))

    processing = original.copy()

    if max(processing.size) > MAX_SIZE:
        processing.thumbnail(
            (MAX_SIZE, MAX_SIZE),
            Image.Resampling.LANCZOS
        )
        _log_image("resized_for_processing", np.array(processing))

    input_buffer = io.BytesIO()
    processing.save(input_buffer, format="PNG")

    output_transparent_bytes = remove(
        input_buffer.getvalue(),
        session=session,
        alpha_matting=False
    )

    with Image.open(io.BytesIO(output_transparent_bytes)) as result:
        foreground = result.convert("RGBA")

    alpha = foreground.getchannel("A")
    alpha = alpha.resize(original_size, Image.Resampling.LANCZOS)

    rgba = np.array(original.convert("RGBA"))
    rgba[:, :, 3] = np.array(alpha)

    img_transparent = refine_edges(
        Image.fromarray(rgba),
        erode_size=1,
        blur_size=3
    )

    white_background = Image.new(
        "RGBA",
        original_size,
        (255, 255, 255, 255)
    )

    final_img = Image.alpha_composite(
        white_background,
        img_transparent
    )

    output = io.BytesIO()
    # Save without EXIF to avoid orientation confusion downstream
    final_img.convert("RGB").save(
        output,
        format="JPEG",
        quality=95,
        dpi=(DPI, DPI)
    )
    output.seek(0)

    _log_image("output", output)
    print(f"[BG DEBUG] remove_background took {time.time() - t0:.1f}s", flush=True)
    return output
