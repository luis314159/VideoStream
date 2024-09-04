import cv2
import zmq
import base64
import numpy as np
from load_ip import load_ip
def main():

    # Load server IP
    server_ip = load_ip()
    print(server_ip)

if __name__ == "__main__":
    # Call the main function with the test flag
    main()
