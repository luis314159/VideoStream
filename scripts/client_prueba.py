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
    
    # Try to connect to the server with retries
    while True:
        try:
            socket.connect(f"tcp://{server_ip}:{server_port}")
            print(f"Connected to server at {server_ip}:{server_port}")
            break  # Exit the loop if the connection is successful
        except Exception as e:
            print(f"Failed to connect to server: {e}. Retrying in 5 seconds...")
            time.sleep(5)

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
        try:
            socket.send(jpg_as_text)
            print("Frame sent to server")

            # Set a timeout for receiving confirmation
            socket.setsockopt(zmq.RCVTIMEO, 5000)  # Timeout of 5 seconds
            message = socket.recv()  # Waiting for confirmation
            print(f"Received reply from server: {message}")
        
        except zmq.Again as e:
            print("No response from server, retrying...")
            continue
        except zmq.ZMQError as e:
            print(f"ZMQ Error occurred: {e}")
            print("Attempting to reconnect to the server...")
            # Close the socket and try to reconnect
            socket.close()
            socket = context.socket(zmq.REQ)
            # Retry connection to server
            while True:
                try:
                    socket.connect(f"tcp://{server_ip}:{server_port}")
                    print(f"Reconnected to server at {server_ip}:{server_port}")
                    break  # Exit the loop if reconnected
                except Exception as e:
                    print(f"Failed to reconnect to server: {e}. Retrying in 5 seconds...")
                    time.sleep(5)
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
