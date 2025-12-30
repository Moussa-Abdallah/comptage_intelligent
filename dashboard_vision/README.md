[//]: # (Image References)

[image1]: ./data/captures/capture_20251213_170942.png "Shapes.sdf"

---

# Dashboard Vision – Smart Parking & Vehicle Detection

Bienvenue dans ce projet ! Ici, nous ne parlons pas simplement de code ou d’un petit script isolé, mais d’une **application complète et interactive** qui combine intelligence artificielle, vision par ordinateur et développement web. L’idée est de créer un système capable de surveiller un parking en temps réel, détecter les véhicules qui y circulent ou y stationnent, et fournir des informations utiles et immédiatement exploitables sur l’état des places disponibles.

Le but concret du projet est simple : lorsqu’un véhicule est détecté dans le flux vidéo, le système vérifie automatiquement **dans quelle place de parking il se trouve**. Si une place est libre, elle reste verte ; si elle est occupée, elle devient rouge. Le système permet ainsi de connaître à tout moment **le nombre de places libres et occupées**. Ces informations sont ensuite affichées sur un **dashboard web développé avec Flask**, où l’utilisateur peut suivre en direct le flux vidéo, capturer des images, lancer ou arrêter la détection, et même définir manuellement les zones de parking à l’aide d’une interface graphique intuitive.

Le dashboard est pensé pour être **simple et clair**. Sur la partie gauche, vous pouvez voir le flux vidéo en direct. Sur la partie droite, des boutons permettent de capturer une image, générer les zones de parking via le GUI, démarrer ou arrêter la détection. En dessous, un panneau indique en temps réel le nombre de places libres et occupées, grâce à des couleurs facilement identifiables : vert pour les places libres et rouge pour les places occupées. Ainsi, même sans expérience technique, un utilisateur peut rapidement visualiser l’état du parking.

Ce projet est **pédagogique et modulaire** : il vous permet de comprendre le fonctionnement d’un pipeline complet, de la capture vidéo à l’affichage sur le dashboard, en passant par la détection des véhicules. Même si vous n’avez jamais utilisé OpenCV, YOLO ou Flask, les explications détaillées pour chaque fichier et chaque ligne de code vous guideront pas à pas.

---

## Objectifs détaillés du projet

L’objectif n’est pas seulement de détecter des véhicules, mais de **transformer le flux vidéo en informations exploitables sur les places de parking**. Le projet se compose de plusieurs étapes :

1. **Capture du flux vidéo** : soit depuis une caméra en direct, soit depuis une vidéo préenregistrée. Cela permet d’obtenir un flux d’images continu sur lequel travailler.

2. **Détection des véhicules** : chaque véhicule présent dans le flux vidéo est identifié par le modèle YOLOv8. Le système peut reconnaître différents types de véhicules et déterminer leur position exacte dans l’image.

3. **Attribution des places de parking** : une fois détecté, le véhicule est comparé aux zones définies pour le parking. Si le véhicule est dans une zone correspondant à une place libre, cette place devient occupée. À l’inverse, lorsqu’une place est vide, elle reste indiquée comme libre. Le système met ainsi à jour en temps réel le nombre de **places libres et occupées**.

4. **Affichage sur le dashboard** : toutes ces informations sont envoyées au dashboard web Flask. Le flux vidéo est affiché avec les véhicules détectés, les places sont colorées selon leur état, et des boutons permettent de capturer des images, lancer/arrêter la détection ou définir les zones de parking. Les utilisateurs peuvent ainsi interagir facilement avec le système et visualiser instantanément l’état du parking.

En résumé, ce projet illustre **comment automatiser la gestion d’un parking en combinant IA et interface web interactive**, tout en restant accessible aux débutants grâce à ses explications détaillées et son interface simple.

---

## Organisation du projet

Le projet est organisé ainsi pour une meilleure compréhension et modularité :

```
dashboard_vision/
│
├─ backend/
│  ├─ app.py                # Serveur Flask et routes principales
│  ├─ capture.py            # Gestion de la capture d'images
│  ├─ detection_byte_track.py # Détection des véhicules et attribution des places
│  ├─ generate_json.py      # GUI pour définir les zones de parking
│
├─ frontend/
│  ├─ templates/index.html  # Page principale du dashboard
│  ├─ static/script.js      # Logique JS côté client
│  ├─ static/style.css      # Style du dashboard
│
├─ data/
│  ├─ captures/             # Captures d’images sauvegardées
│  ├─ CarPark.mp4           # Vidéo de test
│  └─ points/               # Fichiers JSON des zones du parking
│
├─ model/best.pt            # Modèle YOLOv8 entraîné
└─ requirements.txt         # Dépendances Python
```

Chaque dossier a un rôle précis, et cette organisation permet de **modifier facilement une partie du projet sans impacter les autres**.

---

## Démonstration

Pour vous aider à mieux comprendre le fonctionnement du dashboard et de la détection en temps réel, nous avons préparé une démonstration visuelle.  

Vous pouvez voir ci-dessous une capture d’écran du dashboard. Cliquez sur l’image pour accéder directement à la vidéo de démonstration sur YouTube :  

<a href="https://youtu.be/uLnJy93g">
  <img src="data/captures/capture_20251213_170942.png" alt="Cliquez pour voir la démo" width="600">
</a>

Cette vidéo montre plusieurs fonctionnalités clés du projet :  

- Le flux vidéo en direct provenant d’une caméra ou d’une vidéo préenregistrée.  
- La détection des véhicules grâce au modèle YOLOv8.  
- La mise à jour dynamique des places libres et occupées dans le parking.  
- L’utilisation des boutons du dashboard pour capturer des images, lancer ou arrêter la détection et définir les zones de stationnement via l’interface graphique.

> Astuce : même si vous ne disposez pas d’une caméra connectée, vous pouvez tester toutes les fonctionnalités avec une vidéo stockée dans `data/CarPark.mp4`.

---

## Installation

1. **Cloner le projet** :

```bash
git clone <url-du-repo>
cd dashboard_vision
```

2. **Installer Python 3.12+** si ce n’est pas déjà fait.

3. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

4. **Lancer le serveur Flask** :

```bash
python3 backend/app.py
```

5. **Ouvrir le dashboard**
   Dans votre navigateur, allez sur : [http://localhost:5000](http://localhost:5000)

---

## Le code principal : `app.py`

Voici le code complet pour lire une **vidéo existante** et afficher le dashboard :

```python
from flask import Flask, render_template, Response, jsonify
import cv2
import os
import time
import subprocess
from capture import capture_frame
from detection_byte_track import process_frame, parking_status

# CONFIGURATION
VIDEO_PATH = "CarPark.mp4"
CAPTURE_FOLDER = "#"
DETECTION_MODE = False

# Initialisation de Flask
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# Crée le dossier de captures s'il n'existe pas
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# Chargement de la vidéo
def get_video():
    if not os.path.exists(VIDEO_PATH):
        raise RuntimeError(f"Video not found: {VIDEO_PATH}")
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")
    print("[INFO] Video loaded successfully")
    return cap

video = get_video()

# Générateur de frames pour le streaming
def gen_frames():
    global video, DETECTION_MODE
    while True:
        success, frame = video.read()
        if not success:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            time.sleep(0.03)
            continue
        if DETECTION_MODE:
            frame = process_frame(frame)
            cv2.putText(frame, "DETECTION MODE", (900, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        else:
            cv2.putText(frame, "VIDEO MODE", (900,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
        time.sleep(0.03)

# ROUTES FLASK
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/capture", methods=["POST"])
def capture():
    filename = capture_frame(video)
    return jsonify({"status": f"✔ Frame saved: {filename}"})

@app.route("/generate_json", methods=["POST"])
def generate_json():
    subprocess.Popen(["python3", "backend/generate_json.py"])
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

# Lancement du serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True, use_reloader=False)
```

---

### ✅ Explications du code `app.py`

* `from flask import ...` : importe Flask pour créer un serveur web et gérer les routes.
* `import cv2` : OpenCV pour manipuler les images et les vidéos.
* `capture_frame` et `process_frame` : fonctions pour capturer une image ou détecter/tracker des véhicules.
* `VIDEO_PATH` et `CAPTURE_FOLDER` : chemins de la vidéo de test et dossier où enregistrer les captures.
* `DETECTION_MODE` : variable globale pour activer/désactiver la détection.
* `app = Flask(...)` : création du serveur web, en précisant où se trouvent les templates HTML et les fichiers statiques (JS, CSS).
* `get_video()` : ouvre la vidéo avec OpenCV, lève une erreur si impossible.
* `gen_frames()` : boucle infinie qui lit les frames, applique éventuellement la détection, encode chaque frame en JPEG, et les envoie au navigateur pour streaming.
* Les **routes Flask** (`@app.route`) permettent de :

  * afficher le dashboard
  * renvoyer le flux vidéo (`/video_feed`)
  * capturer une image (`/capture`)
  * lancer la détection (`/run_detection`)
  * stopper la détection (`/stop_detection`)
  * récupérer l’état du parking (`/parking_status`).

---

### `capture.py`

```python
import cv2
import datetime
import os

CAPTURE_FOLDER = "/dashboard_vision/data/captures"
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

def capture_frame(video_source):
    if video_source is None:
        return None
    success, frame = video_source.read()
    if not success:
        return None
    filename = os.path.join(CAPTURE_FOLDER,
        f"capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(filename, frame)
    return filename
```

**Explications :**

* `cv2.imwrite()` : sauvegarde la frame actuelle en PNG.
* `datetime` : sert à nommer les fichiers avec la date et l’heure pour éviter les doublons.

---

### `detection_byte_track.py`

```python
import cv2
import numpy as np
import json
from ultralytics import YOLO
import supervision as sv

parking_status = {"free":0, "occupied":0}

with open("Dashboard_vision/bounding_boxes.json", "r") as f:
    data = json.load(f)
parking_slots = [slot["points"] for slot in data]

model = YOLO("/Dashboard_vision/dashboard_vision/model/best.pt")
byte_tracker = sv.ByteTrack(track_activation_threshold=0.25, lost_track_buffer=30,
                            minimum_matching_threshold=0.8, frame_rate=25, minimum_consecutive_frames=3)
byte_tracker.reset()

def mark_slots(frame, detections, names):
    freeslots = 0
    for polygon in parking_slots:
        pts = np.array(polygon, np.int32).reshape((-1,1,2))
        occupied = False
        for xyxy, cls, track_id in zip(detections.xyxy, detections.class_id, detections.tracker_id):
            if int(cls) not in [2,3,4,5,7]:  # Classes véhicules
                continue
            x1,y1,x2,y2 = map(int, xyxy)
            cx,cy = (x1+x2)//2,(y1+y2)//2
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,0),2)
            cv2.putText(frame,f"{names[int(cls)]} ID:{track_id}",(x1,y1-5),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)
            if cv2.pointPolygonTest(pts,(cx,cy),False)>=0:
                occupied=True
                break
        color=(0,0,255) if occupied else (0,255,0)
        cv2.polylines(frame,[pts],True,color,2)
        if not occupied: freeslots+=1
    parking_status["free"]=freeslots
    parking_status["occupied"]=len(parking_slots)-freeslots
    return frame,freeslots,len(parking_slots)-freeslots

def process_frame(frame):
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = detections[np.isin(detections.class_id,[2,3,4,5,7])]
    detections = byte_tracker.update_with_detections(detections)
    frame,free,occupied=mark_slots(frame,detections,results.names)
    return frame
```

**Explications :**

* `YOLO()` : charge le modèle entraîné pour détecter les véhicules.
* `ByteTrack` : suit chaque véhicule pour éviter les doublons.
* `mark_slots()` : dessine les polygones des places et colore selon occupation.
* `process_frame()` : applique détection + tracking + mise à jour du statut du parking.

---

### `script.js`

```javascript
document.getElementById("capture-btn").addEventListener("click", () => {
    fetch("/capture",{method:"POST"}).then(res=>res.json()).then(data=>{
        document.getElementById("status").innerText=data.status;
    }).catch(()=>document.getElementById("status").innerText="Erreur backend");
});

document.getElementById("generate-btn").addEventListener("click",()=>{
    fetch("/generate_json",{method:"POST"}).then(res=>res.json()).then(data=>{
        document.getElementById("status").innerText=data.status;
    }).catch(()=>document.getElementById("status").innerText="Erreur backend");
});

document.getElementById("run-btn").addEventListener("click",()=>{
    fetch("/run_detection",{method:"POST"}).then(res=>res.json()).then(data=>{
        document.getElementById("status").innerText=data.status;
    }).catch(()=>document.getElementById("status").innerText="Erreur backend");
});

document.getElementById("stop-btn").addEventListener("click",()=>{
    fetch("/stop_detection",{method:"POST"}).then(res=>res.json()).then(data=>{
        document.getElementById("status").innerText=data.status;
    }).catch(()=>document.getElementById("status").innerText="Erreur backend");
});

setInterval(()=>{
  fetch("/parking_status").then(res=>res.json()).then(data=>{
      document.getElementById("free").innerText=data.free;
      document.getElementById("occupied").innerText=data.occupied;
  });
},500);
```

**Explications :**

* Récupère les boutons et envoie des requêtes POST au backend.
* Actualise le nombre de places libres/occupées toutes les 0,5 secondes.

---

### `style.css`

```css
body {font-family: Arial; background:#111; color:#eee; margin:0; padding:20px;}
h1{text-align:center;}
#container{display:flex; gap:20px; margin-top:30px;}
#video{flex:3; background:#222; border:2px dashed #555; display:flex; align-items:center; justify-content:center; height:360px;}
#video img{width:100%; height:100%; object-fit:contain;}
#controls{flex:1; background:#1b1b1b; padding:20px; border-radius:8px;}
button{width:100%; padding:10px; margin-bottom:10px; font-size:16px; cursor:pointer;}
.affiche{background:#111; color:#fff; padding:16px 20px; border-radius:12px; width:260px; font-family:"Segoe UI",Tahoma,sans-serif; box-shadow:0 6px 20px rgba(0,0,0,0.35);}
.affiche ul{list-style:none;padding:0;margin:0;}
.affiche li{display:flex; justify-content:space-between; align-items:center; font-size:17px; margin-bottom:12px;}
.affiche li:last-child{margin-bottom:0;}
.affiche span{font-weight:bold; font-size:20px; padding:4px 12px; border-radius:8px; min-width:45px; text-align:center;}
#free{background-color:#2ecc71;color:#000;}
#occupied{background-color:#e74c3c;color:#fff;}
```

**Explications :**

* Style sombre, interface claire.
* Couleurs vert/rouge pour visualiser rapidement l’état des places.

---

### `index.html`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Vision Dashboard</title>
<link rel="stylesheet" href="{{ url_for('static',filename='style.css') }}">
</head>
<body>
<h1>🎥 Vision Dashboard</h1>
<div id="container">
<div id="video"><img src="{{ url_for('video_feed') }}" id="video-stream"></div>
<div id="controls">
<button id="capture-btn">Capture</button>
<button id="generate-btn">Generate JSON</button>
<button id="run-btn">Run Detection</button>
<button id="stop-btn">Stop Detection</button>
<p id="status"></p>
</div>
</div>
<div class="affiche">
<ul>
<li>Places libres: <span id="free">0</span></li>
<li>Places prises: <span id="occupied">0</span></li>
</ul>
</div>
<script src="{{ url_for('static',filename='script.js') }}"></script>
</body>
</
```
