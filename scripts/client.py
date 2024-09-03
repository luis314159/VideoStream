import cv2
import zmq
import time
import base64
from load_ip import load_ip

# Dirección IP y puerto donde el servidor escucha
server_ip = load_ip() # IP de la computadora central
server_port = 5555

# Inicializa la captura de video
cap = cv2.VideoCapture(0)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{server_ip}:{server_port}")

while True:
    # Captura el frame
    ret, frame = cap.read()
    if not ret:
        break

    # Codifica el frame en base64
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)

    # Envía el frame al servidor
    socket.send(jpg_as_text)

    # Espera la confirmación del servidor antes de enviar el siguiente frame
    message = socket.recv()

cap.release()
