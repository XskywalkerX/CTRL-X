import cv2
from contour_utils import find_center, draw_quadrant, check_black_in_quadrant, is_intersection, set_intersection

def process_contours(frame, mask_green, mask_black):
    set_intersection(False)
    h, w, _ = frame.shape

    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    left_detected = False
    right_detected = False

    # GREEN - process all large enough
    for contour in contours_green:
        if cv2.contourArea(contour) < 500:
            continue

        center = find_center(contour)
        if center:
            cx = center[0]
            if cx < w // 2:
                left_detected = True
            else:
                right_detected = True
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (255, 0, 0), -1)
            cv2.putText(frame, f"Green: {center}", (center[0] + 10, center[1] + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            quadrant = draw_quadrant(frame, center)
            check_black_in_quadrant(frame, quadrant)

    # BLACK - only the largest contour
    if contours_black:
        largest_black = max(contours_black, key=cv2.contourArea)
        if cv2.contourArea(largest_black) >= 500:
            center = find_center(largest_black)
            if center:
                cv2.drawContours(frame, [largest_black], -1, (0, 0, 255), 2)
                cv2.circle(frame, center, 5, (255, 255, 0), -1)
                cv2.putText(frame, f"Black: {center}", (center[0] + 10, center[1] + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    direction = ""
    if is_intersection():
        direction = "INTERSECTION: GO FORWARD"
    else:
        if left_detected and right_detected:
            direction = "GO BACK"
        elif right_detected:
            direction = "GO RIGHT"
        elif left_detected:
            direction = "GO LEFT"
        else:
            direction = "GO FORWARD"

    cv2.putText(frame, direction, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
