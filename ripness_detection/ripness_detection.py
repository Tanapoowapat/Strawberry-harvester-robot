import cv2
import numpy as np


def calculate_percent_in_mask(image, mask):
    
    '''
    Parameters:
    image: The image to be analyzed. np.array
    mask: The mask to be applied to the image. np.array 

    Output:
    red_color_percent: The percentage of red pixels in the specified mask. float
    green_color_percent: The percentage of green pixels in the specified mask. float
    mean_val_np: The mean value of each channel in the specified mask. np.array

    
    '''
    
    # Convert color to HSV
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # Calculate the mean value for each channel within the specified mask
    mean_val = cv2.mean(img_hsv, mask=mask)

    # Convert the mean values to a NumPy array
    mean_val_np = np.array(mean_val)

    # Define the target color range in HSV
    # Red mask1 (0-15)
    lower_red = np.array([0, 40, 50])
    upper_red = np.array([15, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    # dark red mask2
    lower_red = np.array([160, 40, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    # Join two masks
    maskRed = mask0 + mask1

    # yellow-green mask
    lower_green = np.array([20,40,50])
    upper_green = np.array([80,255,255])
    maskGreen = cv2.inRange(img_hsv, lower_green, upper_green)


    # Ensure the mask is single-channel (grayscale)
    if len(maskRed.shape) > 2:
        maskRed = cv2.cvtColor(maskRed, cv2.COLOR_BGR2GRAY)

    # Calculate the ratio of red pixels in the specified mask
    ratio_red = cv2.countNonZero(maskRed) / cv2.countNonZero(mask)
    ratio_green = cv2.countNonZero(maskGreen) / cv2.countNonZero(mask)

    # Calculate the color percentage
    red_color_percent = ratio_red * 100
    green_color_percent = ratio_green * 100
    # Round the color_percent to two decimal places
    red_color_percent = np.round(red_color_percent, 2)
    green_color_percent = np.round(green_color_percent, 2)

    return red_color_percent, green_color_percent
