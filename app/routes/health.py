from flask import Blueprint, jsonify
from datetime import datetime, timezone

bp = Blueprint("health", __name__)


@bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})
