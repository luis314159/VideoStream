import cv2
import zmq
import base64
import numpy as np
from load_ip import load_ip

# Dirección IP y puerto donde el servidor escucha

server_ip = load_ip() # IP de la computadora central
server_port = 5555

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://{server_ip}:{server_port}")

# Aquí se cargaría tu modelo de Machine Learning
# model = load_model()

while True:
    # Recibe el frame de la Raspberry Pi
    message = socket.recv()
    jpg_original = base64.b64decode(message)
    np_arr = np.frombuffer(jpg_original, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Procesa el frame con el modelo de inferencia
    # resultado = model.predict(frame)

    # Muestra el frame (opcional)
    cv2.imshow("Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Envía confirmación de recepción a la Raspberry Pi
    socket.send(b"Frame received")

cv2.destroyAllWindows()
