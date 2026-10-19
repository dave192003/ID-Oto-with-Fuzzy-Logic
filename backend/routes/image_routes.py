from flask import Blueprint, request, send_file, jsonify
from services.background_removal import remove_background
from services.image_analysis import analyze_image
from services.fuzzy_enhancement import apply_fuzzy_enhancement
from services.cropping import crop_id_photo
from utils.image_utils import validate_image
import traceback
# Create a blueprint for image processing routes
image_bp = Blueprint("image", __name__)

# Valid ID photo types
VALID_PHOTO_TYPES = ["1x1", "1.5x1.5", "2x2", "passport"]



def process_id_photo(image, photo_type):
    image = validate_image(image)
    print("[DEBUG] Stage 1: Image validated", flush=True)

    image = crop_id_photo(image, photo_type)
    print("[DEBUG] Stage 5: ID photo cropped", flush=True)

    features = analyze_image(image)
    print("[DEBUG] Stage 2: Image analyzed", flush=True)

    image = apply_fuzzy_enhancement(image, features)
    print("[DEBUG] Stage 3: Image enhanced", flush=True)

    image = remove_background(image)
    print("[DEBUG] Stage 4: Background removed", flush=True)

    print(f"[DEBUG] Stage 5: Starting crop, type={photo_type}", flush=True)
    print(f"[DEBUG] Crop input type: {type(image).__name__}", flush=True)

    return image


@image_bp.route("/api/process", methods=["POST"])
def process_image():
    # Check if image was uploaded
    if "image" not in request.files:
        print("[BACKEND] Missing image file", flush=True)
        return jsonify({
            "success": False,
            "error": "Missing image file"
        }), 400

    # Get the photo type
    photo_type = request.form.get("type", "2x2")

    if photo_type not in VALID_PHOTO_TYPES:
        print(f"[BACKEND] Invalid photo type: {photo_type}", flush=True)
        return jsonify({
            "success": False,
            "error": f"Invalid photo type: {photo_type}. Must be one of {VALID_PHOTO_TYPES}"
        }), 400

    # Read the uploaded image
    file = request.files["image"].read()
    print(f"[BACKEND] Image received ({len(file)} bytes)", flush=True)

    try:
        # Run the complete pipeline
        output = process_id_photo(file, photo_type)

        print("[BACKEND] Returning processed image", flush=True)
        return send_file(
            output,
            mimetype="image/png",
            download_name="id-photo.png"
        )

    except ValueError as e:
        print(f"[BACKEND] Processing error: {e}", flush=True)
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[BACKEND] Unexpected error: {e}", flush=True)
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "Unable to process image"
        }), 500

@image_bp.route("/api/remove-bg", methods=["POST"])
def remove_bg():
    print("[BACKEND] Request received", flush=True)
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "Missing image file"
        }), 400

    input_data = request.files["image"].read()
    print(f"[BACKEND] Image received ({len(input_data)} bytes)", flush=True)

    try:
        output = remove_background(input_data)
        print("[BACKEND] Background removed", flush=True)
        return send_file(output, mimetype="image/jpeg")

    except Exception as e:
        print(f"[BACKEND] Error: {e}", flush=True)
        return jsonify({
            "success": False,
            "error": "Unable to remove background"
        }), 500


@image_bp.route("/api/id-crop", methods=["POST"])
def id_crop():
    print("[BACKEND] Request received", flush=True)
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "Missing image file"
        }), 400

    photo_type = request.form.get("type")

    if photo_type not in VALID_PHOTO_TYPES:
        return jsonify({
            "success": False,
            "error": f"Invalid photo type: {photo_type}"
        }), 400

    file = request.files["image"].read()
    print(f"[BACKEND] Image received ({len(file)} bytes)", flush=True)

    try:
        output = crop_id_photo(file, photo_type)
        print("[BACKEND] Image cropped", flush=True)
        return send_file(output, mimetype="image/png")

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[BACKEND] Error: {e}", flush=True)
        return jsonify({
            "success": False,
            "error": "Unable to crop image"
        }), 500