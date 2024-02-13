from ultralytics import YOLO
import cv2

model = YOLO('model/segment/best.pt', task='segment')
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Unable to read frame from camera")
        break

    results = model(frame, stream=True, conf=0.3, device=0)

    for result in results:
        frame = result.plot()

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break