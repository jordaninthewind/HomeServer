from abc import ABC, abstractmethod
from typing import Any


class Sensor(ABC):
    """Base class for all sensors. Subclass and implement `read`."""

    @abstractmethod
    def read(self) -> Any:
        """Return the current reading as a JSON-serialisable value."""
        ...
