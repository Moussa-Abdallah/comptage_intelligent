from flask import Flask, render_template, Response, jsonify
import cv2
import os
import time
import datetime
from capture import capture_frame

import subprocess


app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

VIDEO_PATH = "/home/moussa/Dashboard_vision/dashboard_vision/data/CarPark.mp4"
CAPTURE_FOLDER = "/home/moussa/Dashboard_vision/dashboard_vision/data/captures"

# Crée le dossier captures si n'existe pas
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# Chargement vidéo
def get_video():
    if not os.path.exists(VIDEO_PATH):
        print(f"[ERROR] Video not found: {VIDEO_PATH}")
        return None

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("[ERROR] Cannot open video")
        return None

    print("[INFO] Video loaded successfully")
    return cap

video = get_video()

# Génération des frames pour MJPEG
def gen_frames():
    global video
    while True:
        success, frame = video.read()

        if not success:
            # Fin de vidéo → boucle
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            time.sleep(0.05)
            continue

        # Réduction résolution pour le dashboard
        frame = cv2.resize(frame, (640, 360))

        # Debug visuel
        cv2.putText(frame,
                    "VIDEO STREAM OK",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2)

        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               frame_bytes +
               b"\r\n")

        # Limite FPS pour ne pas saturer CPU
        time.sleep(0.03)  # ~30 FPS

# Routes Flask
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# Bouton capture d'écran
@app.route("/capture", methods=["POST"])
def capture():
    global video
    if video is None:
        return jsonify({"status": "Video not loaded"})

    filename = capture_frame(video)  # ← Utilise ton code réel
    if filename is None:
        return jsonify({"status": "Failed to capture frame"})

    return jsonify({"status": f"✔ Frame saved: {filename}"})

# # Placeholder JSON
# @app.route("/generate_json", methods=["POST"])
# def generate_json():
#     return jsonify({"status": "Generate JSON not implemented yet"})
@app.route("/generate_json", methods=["POST"])
def generate_json():
    try:
        # Lancer le script generate_json.py dans un nouveau processus
        subprocess.run(["python3", "dashboard_vision/backend/generate_json.py"], check=True)
        return jsonify({"status": "GUI ouvert. Place les points et enregistre le JSON dans le dossier data/"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": f"Erreur lors du lancement du GUI : {str(e)}"})
    
# Placeholder run detection
@app.route("/run_detection", methods=["POST"])
def run_detection():
    return jsonify({"status": "Run detection not implemented yet"})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,         # IMPORTANT : pas de double process
        threaded=True,
        use_reloader=False
    )
