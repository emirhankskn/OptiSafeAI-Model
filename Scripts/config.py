import os
import json

def load_video_paths_from_config(config_path=r"C:\Users\kskn1\Desktop\yolo\PythonScripts\video_config.json"):
    """
    Loads video paths from a JSON configuration file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("videos", [])

def load_app_settings():
    """
    Loads any additional application settings if needed.
    Currently returns a basic dictionary for demonstration.
    """
    return {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": True
    }