from datetime import datetime, timezone
from gpiozero import MotionSensor as _PIR
from .base import Sensor
import config


class MotionSensor(Sensor):
    def __init__(self, pin: int = config.MOTION_SENSOR_PIN):
        self._sensor = _PIR(pin)
        self._last_triggered: str | None = None
        self._sensor.when_motion = self._on_motion

    def _on_motion(self) -> None:
        self._last_triggered = datetime.now(timezone.utc).isoformat()

    def read(self) -> dict:
        return {
            "motion": self._sensor.motion_detected,
            "last_triggered": self._last_triggered,
        }
