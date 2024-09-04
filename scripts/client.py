import cv2
import zmq
import time
import base64
from load_ip import load_ip

# Load the server IP
server_ip = load_ip()
server_port = 5555

# Initialize the video capture and zmq socket
cap = cv2.VideoCapture(0)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://{server_ip}:{server_port}")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Compress the frame before sending
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    jpg_as_text = base64.b64encode(buffer)

    # Send the frame to the server
    socket.send(jpg_as_text)

    # Set a timeout for receiving confirmation
    try:
        socket.setsockopt(zmq.RCVTIMEO, 5000)  # Timeout of 5 seconds
        message = socket.recv()  # Waiting for confirmation
    except zmq.Again as e:
        print("No response from server, retrying...")
        continue

cap.release()
socket.close()
