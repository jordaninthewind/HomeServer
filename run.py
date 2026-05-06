from app import create_app, socketio
import config
from werkzeug.debug import DebuggedApplication

app = DebuggedApplication(create_app(), allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    socketio.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)
