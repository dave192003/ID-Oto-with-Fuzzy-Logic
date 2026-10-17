import io
import cv2
import numpy as np
from rembg import remove
from PIL import Image

# Print quality DPI
DPI = 300


def _to_bytes(image):
    """Convert an image (bytes, BytesIO, or numpy array) to raw bytes."""
    if isinstance(image, (bytes, bytearray)):
        return bytes(image)

    if isinstance(image, io.BytesIO):
        return image.getvalue()

    if isinstance(image, np.ndarray):
        # Encode numpy array to bytes
        success, encoded = cv2.imencode(".jpg", image)
        if not success:
            raise ValueError("Failed to encode image")
        return encoded.tobytes()

    raise ValueError("Unsupported image type")

# refine the edges 
def refine_edges(img, erode_size=2, blur_size=3):
    """Refine the alpha edges of an RGBA image."""
    img = img.convert("RGBA")
    rgba = np.array(img)

    alpha = rgba[:, :, 3]

    if erode_size > 0:
        kernel_size = erode_size * 2 + 1
        kernel = np.ones(
            (kernel_size, kernel_size),
            np.uint8
        )
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
    """Remove the background from an image and composite onto white."""
    # Convert to bytes
    image_bytes = _to_bytes(image)

    # Remove background using rembg
    output_transparent_bytes = remove(
    image_bytes,
    alpha_matting=True,
    alpha_matting_foreground_threshold=265,
    alpha_matting_background_threshold=30,
    alpha_matting_erode_size=10
)

    # Open the transparent result
    img_transparent = Image.open(io.BytesIO(output_transparent_bytes)).convert("RGBA")
    img_transparent = refine_edges(
    img_transparent,
    erode_size=1,
    blur_size=2
)

    # Create a white background
    white_background = Image.new("RGBA", img_transparent.size, (255, 255, 255, 255))

    # Composite the subject onto the white background
    final_img = Image.alpha_composite(white_background, img_transparent)

    # Encode as JPEG with print DPI
    output = io.BytesIO()
    final_img.convert("RGB").save(output, format="JPEG", quality=95, dpi=(DPI, DPI))
    output.seek(0)

    return output
