import time
import cv2


window_title = "USB Camera"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

def show_camera():
    print('Start Reading Camera...')
    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    #Init Mask
    mask = cv2.imread('mask.png')
    #Reize Mask to H 480 W 640
    mask = cv2.resize(mask, (640, 480))
    prev_frame_time = 0
    new_frame_time = 0
    if video_capture.isOpened():
        try:
            while True:
                _, frame = video_capture.read()
                #Bitwise And Mask
                frame = cv2.bitwise_and(frame, mask)
                
                #CALCULATE FPS
                new_frame_time = time.time()
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                fps = int(fps)
                print(f'FPS :  {str(fps)}')
                #Draw Rectangle x1 300 x2 340 y1 0 y2 480 
                cv2.rectangle(frame, (300,0), (340,480), (0, 255, 0), 2)
                cv2.imshow(window_title, frame)
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        except Exception as e:
            print(e)
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
