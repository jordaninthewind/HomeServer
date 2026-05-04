import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_ENV", "production") == "development"
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", 0))
