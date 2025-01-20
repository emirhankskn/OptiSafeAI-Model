from Scripts.config import load_video_paths_from_config, load_app_settings
from Scripts.server import VideoServer

def main():
    settings = load_app_settings()

    video_paths = load_video_paths_from_config()

    server = VideoServer(video_paths)
    server.run(
        host=settings["host"],
        port=settings["port"],
        debug=settings["debug"]
    )

if __name__ == "__main__":
    main()
