"""
Print layout service.

Generates a printable layout of multiple ID photos on a single sheet.
"""

import io
from PIL import Image

# Print quality DPI
DPI = 300

# Standard print sheet sizes (in pixels at 300 DPI)
# 4x6 inches = 1200 x 1800 px
# 5x7 inches = 1500 x 2100 px
# A4 = 2480 x 3508 px
PRINT_SHEETS = {
    "4x6": (1200, 1800),
    "5x7": (1500, 2100),
    "a4": (2480, 3508),
}

# Photo dimensions in pixels at 300 DPI
PHOTO_DIMENSIONS = {
    "1x1": (300, 300),
    "1.5x1.5": (450, 450),
    "2x2": (600, 600),
    "passport": (413, 531),
}


def generate_print_layout(image_bytes, photo_type, sheet="4x6", copies=6):
    """
    Generate a printable layout with multiple copies of an ID photo.

    Args:
        image_bytes (bytes): Processed ID photo image bytes.
        photo_type (str): One of "1x1", "1.5x1.5", "2x2", "passport".
        sheet (str): Print sheet size ("4x6", "5x7", "a4").
        copies (int): Number of copies to place on the sheet.

    Returns:
        io.BytesIO: In-memory PNG file of the print layout.
    """
    if photo_type not in PHOTO_DIMENSIONS:
        raise ValueError(f"Invalid photo type: {photo_type}")

    if sheet not in PRINT_SHEETS:
        raise ValueError(f"Invalid sheet size: {sheet}")

    # Open the processed photo
    photo = Image.open(io.BytesIO(image_bytes))
    photo_w, photo_h = photo.size

    # Get sheet dimensions
    sheet_w, sheet_h = PRINT_SHEETS[sheet]

    # Create the print sheet
    sheet_img = Image.new("RGB", (sheet_w, sheet_h), (255, 255, 255))

    # Calculate grid layout
    margin = 50  # pixels margin
    gap = 20  # pixels between photos

    # Calculate how many photos fit
    cols = max(1, (sheet_w - 2 * margin + gap) // (photo_w + gap))
    rows = max(1, (sheet_h - 2 * margin + gap) // (photo_h + gap))

    count = 0
    for row in range(rows):
        for col in range(cols):
            if count >= copies:
                break

            x = margin + col * (photo_w + gap)
            y = margin + row * (photo_h + gap)

            sheet_img.paste(photo, (x, y))
            count += 1

    # Encode as PNG
    output = io.BytesIO()
    sheet_img.save(output, format="PNG", dpi=(DPI, DPI))
    output.seek(0)

    return output