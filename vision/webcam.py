import cv2
from masks import get_masks
from contours import process_contours

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Failed to open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        mask_green, mask_black = get_masks(frame)
        process_contours(frame, mask_green, mask_black)

        cv2.imshow("Contours and Quadrants", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
