import cv2
from process import load_model, load_video, process_frame
from utils.utils import resize_mask


video_path = "test_image/test.mp4"
model_path = 'model/best.onnx'
BATCH_SIZE = 5


def main():
    model = load_model(model_path)
    cap = load_video(video_path)
    _, first_frame = cap.read()
    mask = cv2.imread('mask.png')
    mask = resize_mask(mask, first_frame.shape)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the frame
        frame = cv2.resize(frame, (640, 480))

        # Process the frame
        ripness = process_frame(frame, mask, model)
        print(ripness)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
