
import io
import cv2
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageOps

DPI = 300
MAX_SIZE = 512

# Load BiRefNet Portrait once when the backend starts
BG_SESSION = new_session("birefnet-portrait")


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


def remove_background(image):
    """Remove background using BiRefNet and composite onto white."""
    image_bytes = _to_bytes(image)

    with Image.open(io.BytesIO(image_bytes)) as source:
        img = ImageOps.exif_transpose(source).convert("RGB")

    # Limit the longest side to 512 pixels
    if max(img.size) > MAX_SIZE:
        img.thumbnail(
            (MAX_SIZE, MAX_SIZE),
            Image.Resampling.LANCZOS
        )

    input_buffer = io.BytesIO()
    img.save(input_buffer, format="PNG")
    input_bytes = input_buffer.getvalue()

    # Reuse the existing model session
    output_transparent_bytes = remove(
        input_bytes,
        session=BG_SESSION,
        alpha_matting=False
    )

    img_transparent = Image.open(
        io.BytesIO(output_transparent_bytes)
    ).convert("RGBA")

    img_transparent = refine_edges(
        img_transparent,
        erode_size=1,
        blur_size=2
    )

    white_background = Image.new(
        "RGBA",
        img_transparent.size,
        (255, 255, 255, 255)
    )

    final_img = Image.alpha_composite(
        white_background,
        img_transparent
    )

    output = io.BytesIO()

    final_img.convert("RGB").save(
        output,
        format="JPEG",
        quality=95,
        dpi=(DPI, DPI)
    )

    output.seek(0)
    return output
