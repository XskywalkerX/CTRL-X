import cv2
import numpy as np


intersection_detected = False

def set_intersection(status: bool):
    global intersection_detected
    intersection_detected = status

def is_intersection():
    return intersection_detected

def find_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)
    return None

def draw_quadrant(frame, center):
    h, w, _ = frame.shape

    top_left_x = max(center[0] - 15, 0)
    top_left_y = max(center[1] + 50, 0)
    bottom_right_x = min(center[0] + 15, w)
    bottom_right_y = min(center[1] + 80, h)

    cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 255), 2)

    return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

def check_black_in_quadrant(frame, quadrant):
    x1, y1, x2, y2 = quadrant

    if x1 >= x2 or y1 >= y2:
        print("[!] Invalid quadrant, skipping check.")
        return

    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        print("[!] ROI is empty, skipping.")
        return

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    mask_black = cv2.inRange(hsv_roi, lower_black, upper_black)

    black_pixels = cv2.countNonZero(mask_black)
    total_pixels = mask_black.size
    percent_black = (black_pixels / total_pixels) * 100

    if percent_black > 50:
        set_intersection(True)
        print("Intersection detected in quadrant!")
