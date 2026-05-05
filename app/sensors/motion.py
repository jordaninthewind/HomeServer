from datetime import datetime, timezone
from app.utils import save_snapshot
from typing import Callable
from gpiozero import MotionSensor as _PIR
from .base import Sensor
from app.camera import Camera
import config

camera = Camera()

class MotionSensor(Sensor):
    def __init__(self, pin: int = config.MOTION_SENSOR_PIN):
        self._sensor = _PIR(pin)
        self._last_triggered: str | None = None
        self._callbacks: list[Callable[[dict], None]] = []
        self._sensor.when_motion = self._on_motion

    def on_trigger(self, callback: Callable[[dict], None]) -> None:
        self._callbacks.append(callback)

    def _on_motion(self) -> None:
        self._last_triggered = datetime.now(timezone.utc).isoformat()
        data = self.read()
        frame = camera.snapshot()
        if frame:
            data["frame"] = save_snapshot(frame, config.SNAPSHOT_DIR)
        for cb in self._callbacks:
            cb(data)

    def read(self) -> dict:
        return {
            "motion": self._sensor.motion_detected,
            "last_triggered": self._last_triggered,
        }
