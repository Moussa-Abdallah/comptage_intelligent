import cv2
import numpy as np
import time
import json
from ultralytics import YOLO
import supervision as sv

parking_status = {
    "free": 0,
    "occupied": 0
}
# Charger les places parking
with open("/home/moussa/Dashboard_vision/bounding_boxes.json", "r") as f:
    data = json.load(f)

parking_slots = [slot["points"] for slot in data]

# Charger le modèle YOLO
model = YOLO("/home/moussa/Dashboard_vision/dashboard_vision/model/best.pt")

# Initialiser ByteTrack
byte_tracker = sv.ByteTrack(
    track_activation_threshold=0.25,
    lost_track_buffer=30,
    minimum_matching_threshold=0.8,
    frame_rate=25,
    minimum_consecutive_frames=3
)
byte_tracker.reset()
# LOGIQUE 
def mark_slots(frame, detections, names):
    freeslots = 0

    for polygon in parking_slots:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        occupied = False

        for xyxy, cls, track_id in zip(
            detections.xyxy,
            detections.class_id,
            detections.tracker_id
        ):
            # Classes véhicules (YOLO COCO)
            if int(cls) not in [2, 3, 4, 5, 7]:
                continue

            x1, y1, x2, y2 = map(int, xyxy)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            label = names[int(cls)]
            # Dessiner bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            # Label + ID ByteTrack
            cv2.putText(
                frame,
                f"{label} ID:{track_id}",
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )
            # Test occupation
            if cv2.pointPolygonTest(pts, (cx, cy), False) >= 0:
                occupied = True
                break
        # Dessin place parking
        color = (0, 0, 255) if occupied else (0, 255, 0)
        if not occupied:
            freeslots += 1

        cv2.polylines(frame, [pts], True, color, 2)

    occupied_slots = len(parking_slots) - freeslots

    # Infos globales
    # cv2.putText(frame, f"Free Slots: {freeslots}", (10, 40),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    # cv2.putText(frame, f"Occupied Slots: {occupied_slots}", (10, 80),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return frame,freeslots,occupied_slots

# FLASK ENTRY
def process_frame(frame):
    """
    Reçoit UNE frame
    Retourne UNE frame annotée
    """
    # YOLO inference
    results = model(frame, verbose=False)[0]
    # Convertir vers Supervision
    detections = sv.Detections.from_ultralytics(results)
    # Filtrer véhicules
    detections = detections[np.isin(detections.class_id, [2, 3, 4, 5, 7])]
    # Appliquer ByteTrack
    detections = byte_tracker.update_with_detections(detections)
    frame, free, occupied = mark_slots(frame, detections, results.names)

    parking_status["free"] = free
    parking_status["occupied"] = occupied

    return frame
