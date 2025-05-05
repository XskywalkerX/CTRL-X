import cv2
import numpy as np

def get_masks(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    return mask_green, mask_black
