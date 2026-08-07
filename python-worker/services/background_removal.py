"""
Background removal service.

Uses the rembg library to remove image backgrounds and
composite the subject onto a white background.
"""

import io
from rembg import remove
from PIL import Image

# Print quality DPI
DPI = 300


def remove_background(image_bytes):
    """
    Remove the background from an image and composite onto white.

    Args:
        image_bytes (bytes): Raw image file bytes.

    Returns:
        io.BytesIO: In-memory JPEG file with white background.
    """
    # Remove background using rembg
    output_transparent_bytes = remove(image_bytes)

    # Open the transparent result
    img_transparent = Image.open(
        io.BytesIO(output_transparent_bytes)
    ).convert("RGBA")

    # Create a white background
    white_background = Image.new(
        "RGBA",
        img_transparent.size,
        (255, 255, 255, 255)
    )

    # Composite the subject onto the white background
    final_img = Image.alpha_composite(white_background, img_transparent)

    # Encode as JPEG with print DPI
    output = io.BytesIO()
    final_img.convert("RGB").save(
        output,
        format="JPEG",
        quality=95,
        dpi=(DPI, DPI)
    )
    output.seek(0)

    return output