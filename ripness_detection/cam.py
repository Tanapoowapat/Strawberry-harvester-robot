import cv2
from ultralytics import YOLO


#LOAD MODEL
model = YOLO('model/detection/best.pt')
#LOAD WEBCAM 1 OR 0 for default webcam
cap = cv2.VideoCapture(0)

#READ THE FRAME
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break


    #PROCESS THE FRAME
    results = model(frame, stream=True, half=True, device=0)

    #DISPLAY THE FRAME
    for result in results:
        frame = result.plot()

    cv2.imshow('frame', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break