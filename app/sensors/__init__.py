from .base import Sensor
from .motion import MotionSensor
from typing import Any

_registry: dict[str, Sensor] = {
    "motion": MotionSensor(),
}


def register(sensor_id: str, sensor: Sensor) -> None:
    _registry[sensor_id] = sensor


def get_all_readings() -> dict[str, Any]:
    return {sid: s.read() for sid, s in _registry.items()}
