import numpy as np
import cv2

img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 127, 255, 1)

image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    print(len(approx))
    if len(approx) == 5:
        print("pentagon")
        cv2.drawContours(img, [cnt], 0, 255, -1)
    elif len(approx) == 3:
        print("triangle")
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
    elif len(approx) == 4:
        print("square")
        cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
    elif len(approx) == 9:
        print("half-circle")
        cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
    elif len(approx) > 15:
        print("circle")
        cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)

if __name__ == '__main__':
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
