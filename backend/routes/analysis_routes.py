"""
Route handlers for fuzzy analysis endpoints.

Provides the /api/analyze endpoint that returns the full
fuzzy logic analysis for the fuzzy-analysis page.
"""

from flask import Blueprint, request, jsonify

from services.image_analysis import analyze_image
from services.fuzzy_enhancement import apply_fuzzy_enhancement
from utils.image_utils import validate_image

# Create a blueprint for analysis routes
analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/api/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "Missing image file"
        }), 400

    file = request.files["image"].read()
    print(f"[BACKEND] Image received ({len(file)} bytes)", flush=True)

    try:
        # Validate the image
        img = validate_image(file)

        # Extract features
        features = analyze_image(img)
        print(f"[BACKEND] Image analyzed: {features}", flush=True)

        # Run fuzzy logic pipeline
        from fuzzy_logic.inference import fuzzy_logic
        decision = fuzzy_logic(features)

        # Apply enhancement and analyze the result
        enhanced = apply_fuzzy_enhancement(img, features)
        enhanced_features = analyze_image(enhanced)

        # Build the analysis response
        response = {
            "success": True,
            "original_features": features,
            "processed_features": enhanced_features,
            "parameters": decision["parameters"],
            "fired_rules": decision["fired_rules"],
            "fuzzified": decision["fuzzified"],
            "outputs": decision["outputs"],
        }

        return jsonify(response)

    except ValueError as e:
        print(f"[BACKEND] Validation error: {e}", flush=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[BACKEND] Unexpected error: {e}", flush=True)
        return jsonify({
            "success": False,
            "error": "Unable to analyze image"
        }), 500