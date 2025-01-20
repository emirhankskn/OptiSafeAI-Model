from flask import Flask, Response, jsonify
from video_streamer import StreamManager

class VideoServer:
    """
    Sets up a Flask application, defines routes, and uses StreamManager
    to provide real-time video streams.
    """
    def __init__(self, video_paths):
        self.app = Flask(__name__)
        self.stream_manager = StreamManager(video_paths)
        self._define_routes()

    def _define_routes(self):
        @self.app.route('/video_feed/<video_id>')
        def video_feed(video_id):
            """
            Returns the streaming response for a specific video ID.
            """
            streamer = self.stream_manager.get_streamer(video_id)
            if streamer:
                return Response(streamer.generate_frames(),
                                mimetype='multipart/x-mixed-replace; boundary=frame')
            else:
                return "Video ID not found", 404

        @self.app.route('/list_videos')
        def list_videos():
            """
            Returns a JSON list of available video IDs and their paths.
            """
            video_list = self.stream_manager.list_videos()
            return jsonify(video_list)

    def run(self, host='0.0.0.0', port=5000, debug=True):
        """
        Runs the Flask application.
        """
        self.app.run(host=host, port=port, debug=debug)
