import cv2
import numpy as np
from PIL import Image
import io

DPI = 300


def enhance_image(img, parameters):

    print("===== ENHANCE DEBUG =====", flush=True)
    print("Input shape:", img.shape, flush=True)
    print("Input dtype:", img.dtype, flush=True)
    print("Parameters:", parameters, flush=True)

    denoised = cv2.fastNlMeansDenoisingColored(
        img,
        None,
        parameters["denoise"],
        parameters["denoise"],
        7,
        21
    )

    # Sa ngayon gumamit muna ng stable sharpening kernel
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)

    sharpened = cv2.filter2D(
        denoised,
        -1,
        kernel
    )

    enhanced = cv2.convertScaleAbs(
        sharpened,
        alpha=float(parameters["alpha"]),
        beta=float(parameters["beta"])
    )

    print("Output shape:", enhanced.shape, flush=True)
    print("Min:", enhanced.min(), flush=True)
    print("Max:", enhanced.max(), flush=True)

    return enhanced


def encode_image_png(img_bgr):

    print("===== ENCODE PNG =====", flush=True)
    print("Shape:", img_bgr.shape, flush=True)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(img_rgb)

    output = io.BytesIO()

    pil_img.save(
        output,
        format="PNG",
        dpi=(DPI, DPI)
    )

    output.seek(0)

    print("PNG SIZE:", len(output.getvalue()), flush=True)

    return output