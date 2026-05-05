import subprocess
import threading
import config

_JPEG_SOI = b"\xff\xd8"
_JPEG_EOI = b"\xff\xd9"


class Camera:
    """Singleton that runs rpicam-vid and parses MJPEG frames from its stdout."""

    _instance: "Camera | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "Camera":
        with cls._lock:
            if cls._instance is None:
                inst = super().__new__(cls)
                inst._start()
                cls._instance = inst
        return cls._instance

    def _start(self) -> None:
        self._frame: bytes | None = None
        self._condition = threading.Condition()
        self._proc = subprocess.Popen(
            [
                "rpicam-vid",
                "--timeout", "0",
                "--codec", "mjpeg",
                "--width", str(config.CAMERA_WIDTH),
                "--height", str(config.CAMERA_HEIGHT),
                "--framerate", str(config.CAMERA_FPS),
                "--output", "-",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        self._reader = threading.Thread(target=self._read_frames, daemon=True)
        self._reader.start()

    def _read_frames(self) -> None:
        buf = b""
        while True:
            chunk = self._proc.stdout.read(65536)
            if not chunk:
                break
            buf += chunk
            while True:
                start = buf.find(_JPEG_SOI)
                end = buf.find(_JPEG_EOI, start + 2)
                if start == -1 or end == -1:
                    break
                frame = buf[start : end + 2]
                buf = buf[end + 2 :]
                with self._condition:
                    self._frame = frame
                    self._condition.notify_all()

    def read_frame(self) -> bytes:
        with self._condition:
            self._condition.wait()
            return self._frame

    def snapshot(self, timeout: float = 2.0) -> bytes | None:
        with self._condition:
            if self._frame is not None:
                return self._frame
            self._condition.wait(timeout)
            return self._frame

    def stop(self) -> None:
        self._proc.terminate()
        self._proc.wait()
