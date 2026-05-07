from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from database.queries import save_document
from services.ai_service import generate_document
from services.prompt_service import DocumentRequest


generate_bp = Blueprint("generate", __name__)


@generate_bp.post("/document")
def document():
    try:
        payload = DocumentRequest.model_validate(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"error": "invalid_request", "details": exc.errors()}), 400

    result = generate_document(payload)
    document_id = save_document(result, user_id=payload.user_id)
    result["id"] = document_id
    return jsonify(result)
