import cv2
import numpy as np
from ripness_detection import calculate_percent_in_mask

def extract_contour_and_mask(c):
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

def find_center(box):
    return (int(box[0]) + int(box[1]))//2

def find_strawberry(result):
    red_color_percent = 0
    green_color_percent = 0

    if result.masks is None:
        return None, None
    else:
        img = result.orig_img
        for ci, c in enumerate(result):
            _, mask3ch = extract_contour_and_mask(c)
            isolated = cv2.bitwise_and(mask3ch, img)

            x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
            iso_crop = isolated[y1:y2, x1:x2]
            mask_crop = mask3ch[y1:y2, x1:x2]

            red_color_percent, green_color_percent = calculate_percent_in_mask(iso_crop, mask_crop)
            ripness = ripness_level(red_color_percent, green_color_percent)
            boxes = (x1, y1, x2, y2)
            return ripness, boxes
