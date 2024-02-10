import cv2
import time
from process import load_model, load_webcam, process_frame
from utils.utils import resize_mask

# Constants Model&Frame
WEBCAM_DIVICE = 0 #ใช้ Webcam เปลี่ยนตรงนี้เป็น 0
model_path = "./model/segment/best.pt"
#FRAME_SIZE = (640, 640)


def main():
    print("Load Model...")
    model = load_model(model_path)
    cap = load_webcam(WEBCAM_DIVICE)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    
    # Constants FPS
    prev_frame_time = 0
    new_frame_time = 0

    COUNT = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Process the frame
        frame, ripness, box = process_frame(frame, model)
        if ripness == "Full Ripe" and box is not None:
            COUNT += 1
            print(f"Count: {COUNT}")
            time.sleep(10)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = str(int(fps))
        cv2.putText(frame, "FPS: " + fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow("frame", frame)


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()