from datetime import datetime, timezone
from typing import Callable
import RPi.GPIO as GPIO
from .base import Sensor
import config


class MotionSensor(Sensor):
    def __init__(self, pin: int = config.MOTION_SENSOR_PIN):
        self._pin = pin
        self._last_triggered: str | None = None
        self._callbacks: list[Callable[[dict], None]] = []

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._pin, GPIO.RISING, callback=self._on_motion, bouncetime=300)

    def on_trigger(self, callback: Callable[[dict], None]) -> None:
        self._callbacks.append(callback)

    def _on_motion(self, _channel: int) -> None:
        self._last_triggered = datetime.now(timezone.utc).isoformat()
        data = self.read()
        for cb in self._callbacks:
            cb(data)

    def read(self) -> dict:
        return {
            "motion": bool(GPIO.input(self._pin)),
            "last_triggered": self._last_triggered,
        }

    def cleanup(self) -> None:
        GPIO.remove_event_detect(self._pin)
        GPIO.cleanup(self._pin)
