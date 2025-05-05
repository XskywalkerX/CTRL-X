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
        print("[!] Intersection detected in quadrant!")


def check_black_direction(frame, mask_black, intersection_detected):
    h, w, _ = frame.shape
    region_height = 100
    region_width = 140

    forward_roi = (w//2 - region_width//2, 20, w//2 + region_width//2, 20 + region_height)
    left_roi = (40, h//2 - region_height//2, 40 + region_width, h//2 + region_height//2)
    right_roi = (w - 40 - region_width, h//2 - region_height//2, w - 40, h//2 + region_height//2)

    rois = {
        "forward": forward_roi,
        "left": left_roi,
        "right": right_roi
    }

    for label, (x1, y1, x2, y2) in rois.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    def is_black(roi_coords):
        x1, y1, x2, y2 = roi_coords
        roi = mask_black[y1:y2, x1:x2]
        black_pixels = cv2.countNonZero(roi)
        total_pixels = roi.size
        percent_black = (black_pixels / total_pixels) * 100
        return percent_black > 30

    if intersection_detected:
        cv2.putText(frame, "Direction: GO FORWARD (intersection)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        return

    f = is_black(forward_roi)
    l = is_black(left_roi)
    r = is_black(right_roi)

    if f or (l and r) or (not f and not l and not r):
        direction = "GO FORWARD"
    elif l:
        direction = "GO LEFT"
    elif r:
        direction = "GO RIGHT"
    else:
        direction = "GO FORWARD"

    return direction
