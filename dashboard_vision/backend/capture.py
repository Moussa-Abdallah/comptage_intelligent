# capture.py
import cv2
import datetime
import os

CAPTURE_FOLDER = "/home/moussa/Dashboard_vision/dashboard_vision/data/captures"
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

def capture_frame(video_source):
    """
    Prend une frame depuis video_source et la sauvegarde.
    video_source : cv2.VideoCapture (le flux du dashboard)
    Retourne : chemin du fichier sauvegardé ou None
    """
    if video_source is None:
        return None

    success, frame = video_source.read()
    if not success:
        return None

    # Nom horodaté pour éviter l'écrasement
    filename = os.path.join(
        CAPTURE_FOLDER,
        f"capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    # Sauvegarde de l'image
    cv2.imwrite(filename, frame)

    return filename

# Test rapide depuis ce fichier
if __name__ == "__main__":
    cap = cv2.VideoCapture("images/CarPark.mp4")
    filename = capture_frame(cap)
    if filename:
        print(f"✔ Capture enregistrée sous {filename}")
    else:
        print("❌ Impossible de capturer la frame")
    cap.release()
