"""
Route handlers for image processing endpoints.
"""

from flask import Blueprint, request, send_file, jsonify
import cv2
import numpy as np

from services.background_removal import remove_background
from services.id_crop import crop_id_photo
from services.feature_extraction import analyze_image
from services.enhancement import enhance_image, encode_image_png
from fuzzy_logic.inference import fuzzy_logic
from utils import save_features_to_csv

# Create a blueprint for image processing routes
image_bp = Blueprint("image", __name__)


@image_bp.route("/remove-bg", methods=["POST"])
def remove_bg():
    """Remove the background from an uploaded image."""
    if "image" not in request.files:
        return "Missing image file", 400

    print("REMOVE BG HIT", flush=True)

    input_data = request.files["image"].read()
    output = remove_background(input_data)

    print("REMOVE BG DONE", flush=True)

    return send_file(output, mimetype="image/jpeg")


@image_bp.route("/id-crop", methods=["POST"])
def id_crop():
    """Crop an uploaded image to a standard ID photo size."""
    if "image" not in request.files:
        return "Missing image file", 400

    photo_type = request.form.get("type")

    if photo_type not in ["1x1", "1.5x1.5", "2x2", "passport"]:
        return "Invalid photo type", 400

    print("ID CROP HIT", flush=True)
    print("TYPE:", photo_type, flush=True)

    file = request.files["image"].read()

    try:
        output = crop_id_photo(file, photo_type)
    except ValueError as e:
        return str(e), 400

    print("ID CROP DONE", flush=True)

    return send_file(output, mimetype="image/png")


@image_bp.route("/enhance", methods=["POST"])
def enhance():
    """
    Enhance an uploaded image using the fuzzy logic pipeline.

    Returns the processed image as a PNG file.
    """
    if "image" not in request.files:
        return "Missing image file", 400

    file = request.files["image"].read()

    np_img = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return "Invalid image", 400

    # Extract features
    features = analyze_image(img)
    print("FEATURES:", features, flush=True)

    # Save features for statistical analysis
    save_features_to_csv(features)

    # Run fuzzy logic pipeline
    decision = fuzzy_logic(features)
    parameters = decision["parameters"]
    print("===== DECISION =====", flush=True)
    print(parameters, flush=True)

    # Apply enhancement
    enhanced = enhance_image(img, parameters)

    # Encode and return
    output = encode_image_png(enhanced)

    return send_file(output, mimetype="image/png")


@image_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze an uploaded image and return the full fuzzy logic analysis.

    Returns JSON with:
        - Original image features
        - Enhancement parameters
        - Fired fuzzy rules
        - Fuzzified input values
        - Fuzzy output sets
    """
    if "image" not in request.files:
        return jsonify({"error": "Missing image file"}), 400

    file = request.files["image"].read()

    np_img = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    # Extract features
    features = analyze_image(img)
    print("FEATURES:", features, flush=True)

    # Run fuzzy logic pipeline
    decision = fuzzy_logic(features)

    # Apply enhancement and analyze the result
    enhanced = enhance_image(img, decision["parameters"])
    enhanced_features = analyze_image(enhanced)

    # Build the analysis response
    response = {
        "original_features": features,
        "processed_features": enhanced_features,
        "parameters": decision["parameters"],
        "fired_rules": decision["fired_rules"],
        "fuzzified": decision["fuzzified"],
        "outputs": decision["outputs"],
    }

    return jsonify(response)