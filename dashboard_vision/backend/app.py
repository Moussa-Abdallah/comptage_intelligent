# ==========CODE UTILISANT UNE VIDEO DEJA STOCKER ===========

from flask import Flask, render_template, Response, jsonify
import cv2
import os
import time
import subprocess
from capture import capture_frame
from detection_byte_track import process_frame,parking_status

# CONFIG
VIDEO_PATH = "/home/moussa/Dashboard_vision/dashboard_vision/data/CarPark.mp4" # vidéo unique
CAPTURE_FOLDER = "/home/moussa/Dashboard_vision/dashboard_vision/data/captures"

DETECTION_MODE = False

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# VIDEO LOADER 
def get_video():
    if not os.path.exists(VIDEO_PATH):
        raise RuntimeError(f"Video not found: {VIDEO_PATH}")

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    print("[INFO] Video loaded successfully")
    return cap

video = get_video()


# FRAME GENERATOR
def gen_frames():
    global video, DETECTION_MODE

    while True:
        success, frame = video.read()
        # Boucle vidéo
        if not success:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            time.sleep(0.03)
            continue
        # Resize pour dashboard
        #frame = cv2.resize(frame, (640, 360))

        # MODE DETECTION
        if DETECTION_MODE:
            frame = process_frame(frame)
            cv2.putText(frame, "DETECTION MODE",
                        (900, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2)
        else:
            cv2.putText(frame, "VIDEO MODE",
                        (900, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2)

        # Encode JPEG
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               buffer.tobytes() +
               b"\r\n")

        time.sleep(0.03)  # ~30 FPS
# ROUTES

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/capture", methods=["POST"])
def capture():
    filename = capture_frame(video)
    return jsonify({"status": f"✔ Frame saved: {filename}"})

@app.route("/generate_json", methods=["POST"])
def generate_json():
    # Lance le GUI de placement des points
    subprocess.Popen(["python3", "dashboard_vision/backend/generate_json.py"])
    return jsonify({"status": "GUI ouvert pour placer les polygones"})

@app.route("/run_detection", methods=["POST"])
def run_detection():
    global DETECTION_MODE
    DETECTION_MODE = True
    return jsonify({"status": "Detection started"})

@app.route("/stop_detection", methods=["POST"])
def stop_detection():
    global DETECTION_MODE
    DETECTION_MODE = False
    return jsonify({"status": "Detection stopped"})
@app.route("/parking_status")
def parking_status_api():
    return jsonify(parking_status)

# MAIN 
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )

# ========= CODE PARFAIT QUI AFFICHE LE FLUX VIDEO PROVENANT D'UN CAMERA EXTERNE =========

# from flask import Flask, render_template, Response, jsonify
# import cv2
# import os
# import time
# import subprocess
# from capture import capture_frame
# from detection import process_frame

# # CONFIG
# CAPTURE_FOLDER = "/home/moussa/Dashboard_vision/dashboard_vision/data/captures"
# CAMERA_INDEX = 2   # caméra externe sur /dev/video2

# DETECTION_MODE = False

# app = Flask(
#     __name__,
#     template_folder="../frontend/templates",
#     static_folder="../frontend/static"
# )

# os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# # VIDEO LOADER 
# def get_video():
#     cap = cv2.VideoCapture(CAMERA_INDEX)

#     # Optionnel : fixer résolution et FPS
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#     cap.set(cv2.CAP_PROP_FPS, 30)

#     if not cap.isOpened():
#         raise RuntimeError(f"Cannot open camera index {CAMERA_INDEX}")

#     print(f"[INFO] Camera /dev/video{CAMERA_INDEX} opened successfully")
#     return cap

# video = get_video()


# # FRAME GENERATOR
# def gen_frames():
#     global video, DETECTION_MODE

#     while True:
#         success, frame = video.read()
#         if not success:
#             time.sleep(0.03)
#             continue

#         # MODE DETECTION
#         if DETECTION_MODE:
#             frame = process_frame(frame)
#             cv2.putText(frame, "DETECTION MODE",
#                         (20, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         0.8,
#                         (0, 0, 255),
#                         2)
#         else:
#             cv2.putText(frame, "VIDEO MODE",
#                         (20, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         0.8,
#                         (0, 255, 0),
#                         2)

#         # Encode JPEG
#         ret, buffer = cv2.imencode(".jpg", frame)
#         if not ret:
#             continue

#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" +
#                buffer.tobytes() +
#                b"\r\n")

#         time.sleep(0.03)  # ~30 FPS


# # ROUTES
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/video_feed")
# def video_feed():
#     return Response(
#         gen_frames(),
#         mimetype="multipart/x-mixed-replace; boundary=frame"
#     )

# @app.route("/capture", methods=["POST"])
# def capture():
#     filename = capture_frame(video)
#     return jsonify({"status": f"✔ Frame saved: {filename}"})

# @app.route("/generate_json", methods=["POST"])
# def generate_json():
#     subprocess.Popen(["python3", "dashboard_vision/backend/generate_json.py"])
#     return jsonify({"status": "GUI ouvert pour placer les polygones"})

# @app.route("/run_detection", methods=["POST"])
# def run_detection():
#     global DETECTION_MODE
#     DETECTION_MODE = True
#     return jsonify({"status": "Detection started"})

# @app.route("/stop_detection", methods=["POST"])
# def stop_detection():
#     global DETECTION_MODE
#     DETECTION_MODE = False
#     return jsonify({"status": "Detection stopped"})

# @app.route("/parking_status")
# def parking_status_api():
#     return jsonify(parking_status)


# # MAIN 
# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         debug=False,
#         threaded=True,
#         use_reloader=False
#     )