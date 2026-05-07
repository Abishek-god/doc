from flask import Blueprint, jsonify, request

from services.chart_service import build_chart_payload


charts_bp = Blueprint("charts", __name__)


@charts_bp.post("/generate")
def generate_chart():
    payload = request.get_json(silent=True) or {}
    return jsonify(build_chart_payload(payload))
