import time

import cv2


def image_processing():
    img = cv2.imread('variant-6.png')
    img_weight, img_height = img.shape[:2]
    resized_img = cv2.resize(img, (2*img_height, 2*img_weight), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('Original Image', img)
    cv2.imshow('Resized Image', resized_img)

def video_processing():
    cap = cv2.VideoCapture(1)
    down_points = (640, 480)
    LEFT_HITS = 0
    RIGHT_HITS = 0
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(thresh,
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if i % 5 == 0:
                a = x + (w // 2)
                if a < down_points[0] // 2:
                    LEFT_HITS += 1
                else:
                    RIGHT_HITS += 1
                print("Left Hits:", LEFT_HITS)
                print("Right Hits:", RIGHT_HITS)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()

if __name__ == '__main__':
    image_processing()
    # video_processing()

cv2.waitKey(0)
cv2.destroyAllWindows()