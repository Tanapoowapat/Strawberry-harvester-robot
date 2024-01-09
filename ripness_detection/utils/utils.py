import cv2 

def crops_image(image, box):
    '''
    Prama: image: numpy array
           bbox: [x1, y1, x2, y2]
    Return: ROS of image
    '''
    # Create 3-channel mask
    mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)

    # Isolate object with binary mask
    isolated = cv2.bitwise_and(mask3ch, img)
    x1, y1, x2, y2 = box
    # Crop image to object region 
    image = image[y1:y2, x1:x2]
    mask = mask[y1:y2, x1:x2]

    return image, mask

def draw_box(ripness, image, bbox):
    '''
    Prama:    ripness: float 
              image: numpy array
              bbox: [x1, y1, x2, y2]
    Return: Draw box on image with class + riness_level
    '''

    return None

def get_mouse_cord(event, x, y, flags, param):
    '''
    Prama:    event: mouse event
              x: x cord
              y: y cord
              flags: flags
              param: param
    Return: Draw box on image with class + riness_level
    '''
    if event == cv2.EVENT_MOUSEMOVE:
        print(f'x: {x}, y: {y}')

    return None

def resize_mask(mask, target_size):
    '''
    Prama:    mask: numpy array
              target_size: tuple (width, height)
    Return:   reize mask to target size
    '''
    return cv2.resize(mask, (target_size[0], target_size[1]))