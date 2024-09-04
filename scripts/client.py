import cv2
import zmq
import time
import base64
import argparse
from load_ip import load_ip

def main(test_mode):
    # Load server IP
    server_ip = load_ip()
    server_port = 5555

    # Initialize video capture and zmq socket
    cap = cv2.VideoCapture(0)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{server_ip}:{server_port}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Show the captured frame if test_mode is enabled
        if test_mode:
            cv2.imshow("Client Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
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
    if test_mode:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Argument parser for test flag
    parser = argparse.ArgumentParser(description="Client script to send video stream to server.")
    parser.add_argument('--test', action='store_true', help="Enable test mode to show captured video on the client side.")
    args = parser.parse_args()

    # Call the main function with the test flag
    main(args.test)
