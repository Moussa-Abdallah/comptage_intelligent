# Dashboard Vision – Smart Parking & Vehicle Detection

Bienvenue dans ce projet !  
Ici, on ne parle pas seulement de code, mais d’une vraie application qui relie **IA, caméra en temps réel et interface web**.  
Le but ? Compter et détecter des véhicules dans un parking, puis afficher les résultats sur un **dashboard interactif**.

---

## Objectifs du projet
- Utiliser une caméra (ou une vidéo enregistrée) pour capturer un flux en direct.
- Détecter les véhicules grâce à un modèle YOLO entraîné (`model/best.pt`).
- Suivre les véhicules avec ByteTrack pour éviter les doublons.
- Afficher le tout sur un **dashboard Flask** avec :
  - Flux vidéo en direct
  - Boutons pour activer
  - Capture d’images
  - Outil pour définir des zones (polygones) dans le parking

---

## Organisation du projet
Voici comment le projet est structuré :

- **`dashboard_vision/backend/`**  
  Contient le cœur du système :
  - **`app.py`** : le serveur Flask (point d’entrée du projet)  
  - **`capture.py`** : gestion des captures d’images  
  - **`detection.py`** : logique de détection avec YOLO  
  - **`generate_json.py`** : outil pour placer des polygones et générer `bounding_boxes.json`  
  - **`shared/state.json`** : état partagé du système  

- **`dashboard_vision/data/`**  
  - **`captures/`** : images sauvegardées depuis le dashboard  
  - **`CarPark.mp4`** : vidéo de test  
  - **`points/`** : fichiers liés aux zones du parking  

- **`dashboard_vision/frontend/`**  
  - **`templates/index.html`** : page principale du dashboard  
  - **`static/script.js`** : logique côté client  
  - **`static/style.css`** : style du dashboard  

- **`dashboard_vision/model/best.pt`**  
  Le modèle YOLO entraîné pour la détection des véhicules.

- **`rapport_projet/`**  
  Dossier pour la documentation et le rapport final.
---

## Installation & Lancement
### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd Dashboard_vision
```

### 2. Installer les dépendances
Assurez-vous d’avoir Python 3.12+ et installez :
```bash
pip install -r dashboard_vision/requirements.txt
```

### 3. Lancer le serveur Flask
```bash
python3 dashboard_vision/backend/app.py
```

### 4. Ouvrir le dashboard
Allez sur [http://localhost:5000](http://localhost:5000)  
Vous verrez le flux vidéo et les boutons pour interagir.

---

## Fonctionnalités principales
- **Flux vidéo en direct** : depuis une caméra USB ou une vidéo de test.  
- **Bouton “Run Detection”** : active le mode détection (YOLO + ByteTrack).  
- **Bouton “Stop Detection”** : revient au mode vidéo simple.  
- **Capture d’images** : sauvegarde une frame dans `data/captures/`.  
- **Placement des zones** : ouvre un GUI pour définir les polygones du parking.  

---

## Comment ça marche ?
1. **Capture vidéo** avec OpenCV.  
2. **Détection YOLO** sur chaque frame (ou en mode optimisé).  
3. **Tracking ByteTrack** pour suivre les véhicules.  
4. **Dashboard Flask** qui affiche le flux et permet d’interagir.  

---

## Notes utiles
- Si vous avez plusieurs caméras, vérifiez leur index avec :
  ```bash
  v4l2-ctl --list-devices
  ```
  puis modifiez `CAMERA_INDEX` dans `app.py`.

- Le projet est pensé pour être **modulaire** : vous pouvez remplacer le modèle YOLO, ajouter d’autres trackers, ou enrichir le dashboard.

---

## Conclusion
Ce projet est une **démonstration complète** :  
IA + Vision par ordinateur + Interface web = un système de **smart parking** prêt à être déployé.  

Amusez-vous à tester, modifier, et améliorer. Le code est là pour être exploré, pas juste exécuté.
```