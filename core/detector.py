from ultralytics import YOLO

class PPEDetector():
    def __init__(self):
          self.model = YOLO('best.pt')
          self.PERSONS = [5]
          self.HELMETS = [0]
          self.VESTS = [7]


    def detect(self, frame):
        WANTED = self.PERSONS + self.HELMETS + self.VESTS 

        detections = []

        results = self.model.track(frame, tracker ="bytetrack.yaml", persist=True,  imgsz=320)
        for box in results[0].boxes:
            if int(box.cls[0]) in WANTED:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls = int(box.cls[0])
                cls_name = self.model.names[cls]
                conf = float(box.conf[0])
                track_id = int(box.id[0]) if box.id is not None else None

                detections.append((x1, y1, x2, y2, cls_name, conf, track_id))

        return detections


         