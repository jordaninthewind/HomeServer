import cv2
import config


class Camera:
    """Wraps an OpenCV capture device and yields JPEG frames."""

    def __init__(self, index: int = config.CAMERA_INDEX):
        self._cap = cv2.VideoCapture(index)

    def read_frame(self) -> bytes | None:
        ok, frame = self._cap.read()
        if not ok:
            return None
        _, buf = cv2.imencode(".jpg", frame)
        return buf.tobytes()

    def release(self) -> None:
        self._cap.release()

    def __del__(self):
        self.release()
