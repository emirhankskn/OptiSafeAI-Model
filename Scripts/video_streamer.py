import cv2
from detection import PersonDetector

class VideoStreamer:
    """
    Manages a single video source and uses PersonDetector for detection.
    Responsible for generating frames suitable for streaming.
    """
    def __init__(self, video_id: str, video_path: str, person_detector: PersonDetector, frame_skip: int = 3):
        self.video_id = video_id
        self.video_path = video_path
        self.person_detector = person_detector
        self.frame_skip = frame_skip
        self.cap = cv2.VideoCapture(self.video_path)
        self.frame_count = 0

    def generate_frames(self):
        """
        Yields each processed frame in a format suitable
        for a Flask streaming endpoint (multipart/x-mixed-replace).
        """
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 360))

            if self.frame_count % self.frame_skip == 0:
                processed_frame, process_time = self.person_detector.detect_persons(frame)
                print(f"[Video {self.video_id}] Frame {self.frame_count} processed in {process_time:.3f} seconds")
            else:
                processed_frame = frame

            self.frame_count += 1

            success, buffer = cv2.imencode('.jpg', processed_frame)
            if not success:
                continue

            frame_data = buffer.tobytes()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n'
            )

        self.cap.release()

class StreamManager:
    """
    Manages multiple video sources. Creates and holds VideoStreamer
    instances for each source. Also responsible for referencing a single
    PersonDetector or multiple if desired.
    """
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.streamers = {}
        self.person_detector = PersonDetector()  # A single PersonDetector instance

        self._initialize_streams()

    def _initialize_streams(self):
        for i, path in enumerate(self.video_paths):
            video_id = f"{i+1}"
            streamer = VideoStreamer(
                video_id=video_id,
                video_path=path,
                person_detector=self.person_detector
            )
            self.streamers[video_id] = streamer

    def get_streamer(self, video_id):
        """
        Returns the VideoStreamer instance associated with the given video_id.
        """
        return self.streamers.get(video_id, None)

    def list_videos(self):
        """
        Returns a dictionary mapping "video{index}" to its file path.
        """
        return {f"video{i+1}": path for i, path in enumerate(self.video_paths)}
