from flask import Flask, render_template, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
PHOTO_DIR = 'static/photos'

# Crear carpeta de fotos si no existe
os.makedirs(PHOTO_DIR, exist_ok=True)


def take_photo() :
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(PHOTO_DIR, filename)

    # Usa libcamera si estás en Bullseye o superior
    os.system(f"libcamera-jpeg -o {filepath} --width 640 --height 480 --nopreview")

    return filename


def get_photos() :
    files = sorted(os.listdir(PHOTO_DIR), reverse=True)
    return [f for f in files if f.endswith('.jpg')]


@app.route('/')
def index() :
    photos = get_photos()
    last_photo = photos[0] if photos else None
    return render_template("index.html", last_photo=last_photo, photos=photos)


@app.route('/capture')
def capture() :
    take_photo()
    return redirect(url_for('index'))


import socket

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Servidor disponible en: http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
