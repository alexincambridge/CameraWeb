from flask import Flask, render_template, redirect, url_for
import os
from datetime import datetime
import cv2
import socket

app = Flask(__name__)

PHOTO_DIR = 'static/photos'
os.makedirs(PHOTO_DIR, exist_ok=True)

# Ruta del clasificador Haar para detección de rostros
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def take_photo():
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(PHOTO_DIR, filename)
    os.system(f"libcamera-still -o {filepath} --width 640 --height 480 --nopreview")
    return filename

def get_photos():
    files = sorted(os.listdir(PHOTO_DIR), reverse=True)
    return [f for f in files if f.endswith('.jpg')]

@app.route('/')
def index():
    photos = get_photos()
    last_photo = photos[0] if photos else None
    processed_photos = [f for f in photos if f.startswith('processed_')]
    last_processed = processed_photos[0] if processed_photos else None
    return render_template("index.html", last_photo=last_photo, processed_photo=last_processed, photos=photos)

@app.route('/capture')
def capture():
    take_photo()
    return redirect(url_for('index'))

@app.route('/analyze')
def analyze():
    photos = get_photos()
    if not photos:
        print("[ERROR] No hay fotos para analizar.")
        return redirect(url_for('index'))

    last = os.path.join(PHOTO_DIR, photos[0])
    img = cv2.imread(last)

    if img is None:
        print(f"[ERROR] No se pudo cargar la imagen: {last}")
        return redirect(url_for('index'))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detección de rostros
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Dibujar rectángulos sobre los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    processed_filename = f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = os.path.join(PHOTO_DIR, processed_filename)
    cv2.imwrite(output_path, img)

    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    for file in os.listdir(PHOTO_DIR):
        path = os.path.join(PHOTO_DIR, file)
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error al eliminar {file}: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Servidor disponible en: http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
