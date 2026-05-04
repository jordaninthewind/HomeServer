from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from .routes import health, sensors, stream

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

    @socketio.on("connect")
    def on_connect():
        from .sensors import get_all_readings
        emit("sensor_state", get_all_readings())

    return app
