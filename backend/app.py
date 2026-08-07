"""
ID-Oto Flask Backend - Application entry point.

This module handles application setup, CORS configuration,
and route registration. All business logic is delegated to
the routes, services, and fuzzy_logic packages.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.image_routes import image_bp
from routes.analysis_routes import analysis_bp

app = Flask(__name__)

# Configure CORS for the frontend development server
# Allow all origins in development; restrict in production
#
# Default allowed origins include common dev servers (Live Server on 5501,
# Vite on 5173, etc.). Additional origins can be supplied via the
# CORS_ORIGINS environment variable as a comma-separated list, e.g.:
#   CORS_ORIGINS="http://localhost:5501,http://127.0.0.1:5501"
DEFAULT_CORS_ORIGINS = [
    # VS Code Live Server (default port 5501)
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    # Vite dev server
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Common dev ports
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Allow overriding/adding origins via environment variable (comma-separated)
_env_origins = os.environ.get("CORS_ORIGINS", "")
if _env_origins:
    DEFAULT_CORS_ORIGINS.extend(
        origin.strip() for origin in _env_origins.split(",") if origin.strip()
    )

CORS(app, resources={
    r"/api/*": {
        "origins": DEFAULT_CORS_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
    }
})

# Register API blueprints
app.register_blueprint(image_bp)
app.register_blueprint(analysis_bp)


@app.route("/")
def home():
    """Health check endpoint."""
    return "ID-Oto Flask Backend running"


@app.route("/health")
def health():
    """Health check endpoint returning JSON status."""
    return jsonify({"status": "ok", "service": "id-oto-backend"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)