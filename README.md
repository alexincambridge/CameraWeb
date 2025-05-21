# Instrucciones para Raspberry Pi Zero (OS Lite)

1. Asegúrate de que la cámara esté habilitada:
   sudo raspi-config → Interfaces → Camera → Enable

2. Instala dependencias:
   sudo apt update
   sudo apt install python3-flask python3-pip libcamera-apps -y

3. Ejecuta la app:
   python3 app.py

4. Abre en tu navegador desde otra máquina:
   http://<IP_de_tu_raspberry>:5000

   Puedes obtener la IP con: hostname -I

5. Las fotos se guardarán en: static/photos/
