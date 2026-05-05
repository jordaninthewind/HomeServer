import threading
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from .routes import health, sensors, stream
import config

socketio = SocketIO(async_mode="threading", cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio.init_app(app)

    app.register_blueprint(health.bp)
    app.register_blueprint(sensors.bp)
    app.register_blueprint(stream.bp)

    from .sensors import _registry
    motion = _registry.get("motion")
    if motion:
        motion.on_trigger(lambda data: socketio.emit("motion", data))

        def _save_motion_snapshot(_data):
            from .camera import Camera
            from .utils import save_snapshot
            frame = Camera().snapshot()
            if frame:
                save_snapshot(frame, config.SNAPSHOT_DIR)

        motion.on_trigger(_save_motion_snapshot)

    def _timelapse_loop():
        import time
        from .camera import Camera
        from .utils import save_snapshot
        while True:
            time.sleep(config.TIMELAPSE_INTERVAL)
            frame = Camera().snapshot()
            if frame:
                save_snapshot(frame, config.SNAPSHOT_DIR, prefix="timelapse")

    t = threading.Thread(target=_timelapse_loop, daemon=True)
    t.start()

    @socketio.on("connect")
    def on_connect():
        from .sensors import get_all_readings
        emit("sensor_state", get_all_readings())

    return app
