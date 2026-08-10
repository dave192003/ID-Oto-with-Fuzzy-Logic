import io
import cv2
import numpy as np
from PIL import Image
# Print quality DPI
DPI = 300

def validate_image(image):

    if isinstance(image, np.ndarray):
        return image

    if isinstance(image, io.BytesIO):
        image = image.getvalue()

    if isinstance(image, (bytes, bytearray)):
        np_img = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image file")
        return img

    raise ValueError("Unsupported image type")


def encode_image_png(img_bgr):
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

# This is for collecting Image features data only for better fuzzy logic membersgip calculation. This is only temprory
def save_features_to_csv(features, filename="image_features.csv"):
    import os
    import csv

    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Brightness",
                "Contrast",
                "Sharpness",
                "Noise"
            ])

        writer.writerow([
            features["brightness"],
            features["contrast"],
            features["sharpness"],
            features["noise"]
        ])