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
    print(f"Connecting to server at {server_ip}:{server_port}")

    # Initialize video capture and zmq socket
    cap = cv2.VideoCapture(1)
    
    # Give some time for the camera to initialize
    time.sleep(2)

    if not cap.isOpened():
        print("Failed to open camera")
        return

    print("Getting context and socket variable")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    
    try:
        socket.connect(f"tcp://{server_ip}:{server_port}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Show the captured frame if test_mode is enabled
        if test_mode:
            cv2.imshow("Client Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Test mode: Exiting on 'q' key")
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
            print(f"Received reply from server: {message}")
        except zmq.Again as e:
            print("No response from server, retrying...")
            continue

    # Clean up
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
