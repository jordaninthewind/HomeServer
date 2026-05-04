from flask import Blueprint, Response
from app.camera import Camera

bp = Blueprint("stream", __name__, url_prefix="/stream")


def _mjpeg_frames():
    camera = Camera()
    while True:
        frame = camera.read_frame()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )


@bp.get("/video")
def video_feed():
    return Response(
        _mjpeg_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )
