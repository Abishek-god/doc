import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.auth import auth_bp
from api.charts import charts_bp
from api.export import export_bp
from api.generate import generate_bp
from api.images import images_bp
from api.templates import templates_bp


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:5500").split(",")
    CORS(
        app,
        resources={r"/api/*": {"origins": [origin.strip() for origin in allowed_origins if origin.strip()]}},
        supports_credentials=True,
    )

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[os.getenv("RATE_LIMIT", "120 per hour")],
        storage_uri=os.getenv("RATE_LIMIT_STORAGE_URI", "memory://"),
    )

    app.register_blueprint(generate_bp, url_prefix="/api/generate")
    app.register_blueprint(export_bp, url_prefix="/api/export")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(charts_bp, url_prefix="/api/charts")
    app.register_blueprint(images_bp, url_prefix="/api/images")
    app.register_blueprint(templates_bp, url_prefix="/api/templates")

    @app.get("/api/health")
    @limiter.exempt
    def health():
        return jsonify(
            {
                "status": "ok",
                "service": "ai-workspace-backend",
                "aiProvider": "nvidia" if os.getenv("NVIDIA_API_KEY") else "local-fallback",
                "database": "supabase" if os.getenv("SUPABASE_URL") else "not-configured",
            }
        )

    @app.errorhandler(429)
    def rate_limit_handler(error):
        return jsonify({"error": "rate_limit_exceeded", "message": str(error.description)}), 429

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "not_found", "message": "Route not found."}), 404

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
