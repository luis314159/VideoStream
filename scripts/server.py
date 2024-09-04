import cv2
import zmq
import base64
import numpy as np
import argparse
import time

def main(record_flag):
    # Setup ZMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    
    server_ip = "0.0.0.0"  # Listen on all network interfaces
    server_port = 5555
    print(f"Starting server at {server_ip}:{server_port}")
    
    socket.bind(f"tcp://{server_ip}:{server_port}")
    
    # Video writer for recording
    out = None

    while True:
        try:
            # Receive and decode the frame
            message = socket.recv()
            jpg_as_text = base64.b64decode(message)
            npimg = np.frombuffer(jpg_as_text, dtype=np.uint8)
            frame = cv2.imdecode(npimg, 1)

            # Show the frame
            cv2.imshow("Server Video Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting server on 'q' key")
                break

            # Save the frame if recording is enabled
            if record_flag:
                if out is None:
                    # Initialize video writer if it hasn't been initialized yet
                    frame_height, frame_width, _ = frame.shape
                    out = cv2.VideoWriter(f"recorded_video_{int(time.time())}.avi", 
                                          cv2.VideoWriter_fourcc(*"XVID"), 
                                          20, 
                                          (frame_width, frame_height))
                out.write(frame)

            # Send a confirmation back to the client
            socket.send(b"Frame received and processed")

        except Exception as e:
            print(f"Error occurred: {e}")
            break

    # Cleanup
    if out:
        out.release()
    cv2.destroyAllWindows()
    socket.close()

if __name__ == "__main__":
    # Argument parser for recording flag
    parser = argparse.ArgumentParser(description="Server script to receive video stream from client and optionally record it.")
    parser.add_argument('--record', action='store_true', help="Enable recording of the received video stream.")
    args = parser.parse_args()

    # Call the main function with the record flag
    main(args.record)
