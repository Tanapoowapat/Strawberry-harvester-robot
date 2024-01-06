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