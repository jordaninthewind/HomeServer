import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_ENV", "production") == "development"
CAMERA_WIDTH = int(os.getenv("CAMERA_WIDTH", 1280))
CAMERA_HEIGHT = int(os.getenv("CAMERA_HEIGHT", 720))
CAMERA_FPS = int(os.getenv("CAMERA_FPS", 30))

MOTION_SENSOR_PIN = int(os.getenv("MOTION_SENSOR_PIN", 17))
