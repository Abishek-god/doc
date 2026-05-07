from flask import Blueprint, jsonify, request, send_file

from services.export_service import create_export


export_bp = Blueprint("export", __name__)


@export_bp.post("/<export_type>")
def export_document(export_type: str):
    payload = request.get_json(silent=True) or {}
    if export_type not in {"pdf", "docx", "pptx"}:
        return jsonify({"error": "unsupported_export", "message": "Use pdf, docx, or pptx."}), 400

    try:
        file_path = create_export(export_type, payload)
    except ValueError as exc:
        return jsonify({"error": "invalid_document", "message": str(exc)}), 400

    return send_file(file_path, as_attachment=True)


@export_bp.post("/record")
def record_export():
    payload = request.get_json(silent=True) or {}
    return jsonify({"status": "queued", "export": payload})
