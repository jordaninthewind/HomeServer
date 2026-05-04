from flask import Flask
from flask_cors import CORS
from .routes import health, sensors, stream


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(health.bp)
    app.register_blueprint(sensors.bp)
    app.register_blueprint(stream.bp)

    return app
