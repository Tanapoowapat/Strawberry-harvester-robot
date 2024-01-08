import cv2
from ultralytics import YOLO
from process import load_model, load_video, process_frame
from utils.utils import get_mouse_cord


video_path = "test_image/test.mp4"
model_path = 'model/best.onnx'
mask = cv2.imread('mask.png')

def main():
    

    model = load_model(model_path)
    cap = load_video(video_path)
    # Get the frame width and height
    cv2.namedWindow('Strwberry Ripeness Detection')
    cv2.setMouseCallback('Strwberry Ripeness Detection', get_mouse_cord)


    while True:
        ret, frame = cap.read()

        # Resize the frame
        frame = cv2.resize(frame, (640, 640))
        frame_height, frame_width, _ = frame.shape

        if not ret:
            break

        
        red_percent, green_percent, frame_ = process_frame(frame, mask, frame_width, frame_height, model)

        print(f'Red : {red_percent}, Green : {green_percent}')
        
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
