import cv2
import numpy as np
import time
import json
from ultralytics import YOLO

# Initialisation
with open("/home/moussa/Dashboard_vision/bounding_boxes.json", "r") as f:
    data = json.load(f)

parking_slots = [slot["points"] for slot in data]

model = YOLO("/home/moussa/Dashboard_vision/dashboard_vision/model/best.pt")

last_call_time = time.time()
prevFreeslots = 0

# LOGIQUE
def mark_slots(frame, boxes, clss, names):
    global last_call_time, prevFreeslots
    freeslots = 0

    for polygon in parking_slots:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        occupied = False

        for box, cls in zip(boxes, clss):
            label = names[int(cls)]
            if int(cls) in [2, 3, 5, 7]:
                x1, y1, x2, y2 = box
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

                cv2.rectangle(frame, (int(x1), int(y1)),
                              (int(x2), int(y2)), (255, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                if cv2.pointPolygonTest(pts, (cx, cy), False) >= 0:
                    occupied = True
                    break

        color = (0, 0, 255) if occupied else (0, 255, 0)
        if not occupied:
            freeslots += 1

        cv2.polylines(frame, [pts], True, color, 2)

    occupied_slots = len(parking_slots) - freeslots

    cv2.putText(frame, f"Free Slots: {freeslots}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Occupied Slots: {occupied_slots}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return frame

# POINT D’ENTRÉE POUR FLASK
def process_frame(frame):
    """
    Cette fonction est appelée par Flask
    Elle reçoit UNE frame
    Elle retourne UNE frame traitée
    """
    results = model(frame)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    clss = results[0].boxes.cls.cpu().numpy()
    names = results[0].names

    return mark_slots(frame, boxes, clss, names)
