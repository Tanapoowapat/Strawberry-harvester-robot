import cv2
import numpy as np
from ripness_detection import calculate_percent_in_mask
from utils.utils import calculate_centroid

def extract_contour_and_mask(result):
    """Extract contour and mask from the result."""
    contour = result.masks.xy.pop().astype(np.int32).reshape(-1, 1, 2)

    # Draw contour onto mask
    b_mask = np.zeros(result.orig_img.shape[:2], np.uint8)
    _ = cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)

    mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)

    return b_mask, mask3ch

def ripeness_level(red_percent, green_percent):
    """Determine ripeness level based on color percentages."""
    if red_percent >= 80 and green_percent < 10:
        return 'FullRipe'
    elif 80 < red_percent >= 70 and green_percent < 20:
        return 'Ripe'
    elif 70 < red_percent >= 50 and green_percent < 40:
        return 'MediumRipe'
    elif 50 < red_percent >= 30 and green_percent < 60:
        return 'SmallRipe'
    elif 30 < red_percent >= 10 or green_percent < 80:
        return 'Unripe'

def find_horizon_center(box):
    """Find the Horizontal Center of the box."""
    return (int(box[0]) + int(box[2])) // 2

def find_strawberry(result, input_ripeness):
    """Find strawberries with the specified ripeness level."""
    strawberries = []
    img = result.orig_img
    for _, c in enumerate(result):
        _, mask3ch = extract_contour_and_mask(c)
        isolated = cv2.bitwise_and(mask3ch, img)

        x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
        iso_crop = isolated[y1:y2, x1:x2]
        mask_crop = mask3ch[y1:y2, x1:x2]

        red_color_percent, green_color_percent = calculate_percent_in_mask(iso_crop, mask_crop)
        ripeness = ripeness_level(red_color_percent, green_color_percent)
        boxes = (x1, y1, x2, y2)

        if ripeness == input_ripeness:
            _, center_y = calculate_centroid(boxes)
            pos_y = 16 + (10 - (center_y * 0.0264583333))
            strawberries.append(pos_y)
            
    return strawberries
            
def process_frame(result, ripeness):
    """Process the frame and find strawberries with the specified ripeness level."""
    strawberries = find_strawberry(result, ripeness)
    return strawberries
