import os
from datetime import datetime, timezone

def save_snapshot(frame: bytes, directory: str, prefix: str = "motion") -> str:
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(directory, f"{prefix}_{timestamp}.jpg")
    with open(path, "wb") as f:
        f.write(frame)
    return path
