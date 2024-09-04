import cv2
import zmq
import base64
import numpy as np
from load_ip import load_ip

# Load server IP
server_ip = load_ip()
server_port = 5555

# Initialize zmq socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://{server_ip}:{server_port}")

while True:
    try:
        # Receive the frame
        message = socket.recv()
        jpg_original = base64.b64decode(message)
        np_arr = np.frombuffer(jpg_original, dtype=np.uint8)

        # Decode the image
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if frame is None:
            print("Failed to decode frame")
            continue

        # Display the frame
        cv2.imshow("Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Send confirmation back to client
        socket.send(b"Frame received")

    except Exception as e:
        print(f"Error: {e}")
        break

cv2.destroyAllWindows()
socket.close()
