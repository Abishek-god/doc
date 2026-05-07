from flask import Blueprint, jsonify, request

from database.supabase import get_supabase_client


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/session")
def session():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"authenticated": False}), 401

    client = get_supabase_client()
    if not client:
        return jsonify({"authenticated": True, "mode": "frontend-managed"})

    try:
        user = client.auth.get_user(token)
        return jsonify({"authenticated": True, "user": user.user.model_dump()})
    except Exception as exc:
        return jsonify({"authenticated": False, "message": str(exc)}), 401
