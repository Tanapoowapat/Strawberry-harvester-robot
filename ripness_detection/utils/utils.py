import time

def fps(new_frame_time, prev_frame_time):
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    print(f'FPS :  {str(fps)}')
    return prev_frame_time