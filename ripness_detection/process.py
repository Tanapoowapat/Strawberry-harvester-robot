import time
import cv2
import numpy as np
from ripness_detection import calculate_percent_in_mask
from utils.utils import calculate_centroid
import arduio_connect as ac
import time



def extract_contour_and_mask(c):
    '''Extract contour and mask from the result
        Args: c: result from model
        Returns: b_mask: binary mask
    '''
    
    contour = c.masks.xy.pop()
    contour = contour.astype(np.int32)
    contour = contour.reshape(-1, 1, 2)

    # Draw contour onto mask
    b_mask = np.zeros(c.orig_img.shape[:2], np.uint8)
    _ = cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)

    mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)

    return b_mask, mask3ch

def ripness_level(red_percent, green_percent):
    if red_percent >= 80 and green_percent < 10:
        return 'Full Ripe'
    elif 80 < red_percent >= 70 and green_percent < 20:
        return 'Ripe'
    elif 70 < red_percent >= 50 and green_percent < 40:
        return 'Medium Ripe'
    elif 50 < red_percent >= 30 and green_percent < 60:
        return 'Small Ripe'
    elif 30 < red_percent >= 10 or green_percent < 80:
        return 'Unripe'

def find_horizon_center(box):
    '''Find the Horizontal Center of the box
       Args: box: tuple of (x1, y1, x2, y2)
    '''
    return (int(box[0]) + int(box[2]))//2

def process_frame(result):
    red_color_percent = 0
    green_color_percent = 0
    img = result.orig_img
    for _, c in enumerate(result):
            _, mask3ch = extract_contour_and_mask(c)
            isolated = cv2.bitwise_and(mask3ch, img)

            x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
            iso_crop = isolated[y1:y2, x1:x2]
            mask_crop = mask3ch[y1:y2, x1:x2]

            red_color_percent, green_color_percent = calculate_percent_in_mask(iso_crop, mask_crop)
            ripness = ripness_level(red_color_percent, green_color_percent)
            boxes = (x1, y1, x2, y2)

            if ripness == "Full Ripe":
                center_x, center_y = calculate_centroid(boxes)
                #Draw the circle
                cv2.circle(img, (center_x, center_y-100), 5, (0, 255, 0), -1)
                print(f'Center X : {center_x*0.0264583333} Center Y : {center_y*0.0264583333}')
                #Draw the text
                cv2.putText(img, ripness, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #Send data to arduino
                print(ac.send_data(center_y))