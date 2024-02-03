import cv2

#LOAD WEBCAM 1 OR 0 for default webcam
cap = cv2.VideoCapture(1)

#READ THE FRAME
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    cv2.imshow('frame', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break