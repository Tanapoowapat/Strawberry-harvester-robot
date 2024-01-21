import cv2
from process import load_model, load_video, process_frame
from utils.utils import resize_mask

video_path = "test_image/test.mp4"
model_path = "model/best.tflite"
FRAME_SIZE = (640, 640)

def main():
    model = load_model(model_path)
    cap = load_video(video_path)
    mask = cv2.imread('mask.png')
    mask = resize_mask(mask, (FRAME_SIZE[0], FRAME_SIZE[1]))

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the frame to match the model's expected input size
        frame = cv2.resize(frame, (FRAME_SIZE[0], FRAME_SIZE[1]))

        # Process the frame
        ripeness = process_frame(frame, mask, model)
        print(ripeness)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()