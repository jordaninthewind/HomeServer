from .base import Sensor
from typing import Any


# Register sensors here as you add them.
# Each entry maps a sensor_id to a Sensor instance.
_registry: dict[str, Sensor] = {}


def register(sensor_id: str, sensor: Sensor) -> None:
    _registry[sensor_id] = sensor


def get_all_readings() -> dict[str, Any]:
    return {sid: s.read() for sid, s in _registry.items()}
