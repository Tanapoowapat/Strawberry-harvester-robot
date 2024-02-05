import cv2
import time
from process import load_model, load_webcam, process_frame
from utils.utils import resize_mask

WEBCAM_DIVICE = 'test_image/test.mp4' #ใช้ Webcam เปลี่ยนตรงนี้เป็น 0
model_path = "model/best.pt"
FRAME_SIZE = (640, 640)

def main():
    print("Load Model...")
    model = load_model(model_path)
    cap = load_webcam(WEBCAM_DIVICE)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    mask = cv2.imread('mask.png')
    mask = resize_mask(mask, (FRAME_SIZE[0], FRAME_SIZE[1]))
    # Variables for calculating FPS
    start_time = time.time()
    frames_count = 0
    COUNT = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Resize the frame to match the model's expected input size
        frame = cv2.resize(frame, (FRAME_SIZE[0], FRAME_SIZE[1]))

        # Calculate FPS
        frames_count += 1
        elapsed_time = time.time() - start_time
        fps = frames_count / elapsed_time
        print(f"FPS: {fps:.2f}")
        # Process the frame
        ripness, box = process_frame(frame, mask, model)
        if ripness == "Full Ripe" and box is not None:
            COUNT += 1
            print(f"Full Ripe: {COUNT}")
            time.sleep(10)     
            
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()