import time

def fps(new_frame_time, prev_frame_time):
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    print(f'FPS :  {str(fps)}')
    return prev_frame_time

def calculate_centroid(bbox):
    '''
    Calculate the centroid of the bounding box

    Args:
    bbox : tuple
        (x1, y1, x2, y2)

    Returns:
        centroid
    '''
    x1, y1, x2, y2 = bbox
    x = (x1 + x2) // 2
    y = (y1 + y2) // 2
    return x, y