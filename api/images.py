from flask import Blueprint, jsonify, request

from services.image_service import generate_image


images_bp = Blueprint("images", __name__)


@images_bp.post("/generate")
def image():
    payload = request.get_json(silent=True) or {}
    prompt = str(payload.get("prompt", "")).strip()
    if len(prompt) < 3:
        return jsonify({"error": "invalid_prompt", "message": "Prompt must be at least 3 characters."}), 400
    return jsonify(generate_image(prompt, payload.get("style", "modern editorial")))
