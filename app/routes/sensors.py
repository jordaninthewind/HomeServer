from flask import Blueprint, jsonify
from app.sensors import get_all_readings

bp = Blueprint("sensors", __name__, url_prefix="/sensors")


@bp.get("/")
def list_sensors():
    return jsonify(get_all_readings())


@bp.get("/<sensor_id>")
def get_sensor(sensor_id: str):
    readings = get_all_readings()
    if sensor_id not in readings:
        return jsonify({"error": f"sensor '{sensor_id}' not found"}), 404
    return jsonify({sensor_id: readings[sensor_id]})
