import time
import cv2
from ultralytics import YOLO

class PersonDetector:
    """
    Loads and uses a YOLO model to detect persons in a given frame.
    Focuses solely on detection (Single Responsibility Principle).
    """
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model_path = model_path
        self.model = YOLO(self.model_path)

    def detect_persons(self, frame):
        """
        Detects persons (class 0) in the given frame using the YOLO model.
        Draws bounding boxes for each detected person.
        Returns the processed frame and the processing time.
        """
        start_time = time.time()
        results = self.model(frame, verbose=False)

        for result in results[0].boxes:
            if int(result.cls) == 0:  # class 0 (person)
                bbox = result.xyxy[0].tolist()
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        process_time = time.time() - start_time
        return frame, process_time
