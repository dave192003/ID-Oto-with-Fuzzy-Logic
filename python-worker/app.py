"""
ID-Oto Python Worker - Flask application entry point.

This module only handles application setup and route registration.
All business logic is delegated to the services and fuzzy_logic packages.
"""

from flask import Flask, jsonify
from routes.image_routes import image_bp

app = Flask(__name__)

# Register API blueprints
app.register_blueprint(image_bp)


@app.route("/")
def home():
    """Health check endpoint."""
    return "Python worker running"


@app.route("/health")
def health():
    """Health check endpoint returning JSON status."""
    return jsonify({"status": "ok", "service": "python-worker"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)