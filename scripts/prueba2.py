import cv2

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('Test Camera', frame)
    if cv2.waitKey(1) == ord('q'):
        print("Q pressed camara will be closed")
        break 

cap.release()
cv2.destroyAllWindows()
