from flask import Flask, render_template, Response
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# Ruta de modelo Haar Cascade
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

# Crear carpeta de videos si no existe
VIDEO_DIR = 'static/videos'
os.makedirs(VIDEO_DIR, exist_ok=True)

# Iniciar la cámara
camera = cv2.VideoCapture(0)

# Configurar video writer (se inicializa al primer frame)
video_writer = None
output_path = None

def generate_frames():
    global video_writer, output_path

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Detección de rostro
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Inicializar grabación solo una vez
        if video_writer is None:
            filename = datetime.now().strftime("video_%Y%m%d_%H%M%S.mp4")
            output_path = os.path.join(VIDEO_DIR, filename)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            frame_size = (int(camera.get(3)), int(camera.get(4)))
            video_writer = cv2.VideoWriter(output_path, fourcc, 20.0, frame_size)

        # Escribir el frame al archivo de video
        video_writer.write(frame)

        # Codificar para streaming web
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("[INFO] Servidor Flask iniciando en http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=False)
