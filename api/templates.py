from flask import Blueprint, jsonify

from services.prompt_service import TEMPLATE_LIBRARY


templates_bp = Blueprint("templates", __name__)


@templates_bp.get("/")
def list_templates():
    return jsonify({"templates": TEMPLATE_LIBRARY})
