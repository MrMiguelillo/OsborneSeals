import cv2
import numpy as np


def do_nothing(x):
    pass


# def canny_detection(min_t, canny_src):
#     blurred = cv2.GaussianBlur(canny_src, (5, 5), 0)

img = cv2.imread('../imgs/IMG_0003.png')
sub_img = img[0:1800, 0:1800]
# img_gray = sub_img.copy()
edges = sub_img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(img_gray, (5, 5), 0)
# cv2.namedWindow('image_window', cv2.WINDOW_NORMAL)
cv2.namedWindow('result_window', cv2.WINDOW_NORMAL)

cv2.createTrackbar('Min Threshold', 'result_window', 0, 100, do_nothing)
cv2.createTrackbar('Max Threshhold', 'result_window', 0, 500, do_nothing)

while 1:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # cv2.imshow('image_window', sub_img)
    cv2.imshow('result_window', edges)

    low_thresh = cv2.getTrackbarPos('Min Threshold', 'result_window')
    max_thresh = cv2.getTrackbarPos('Max Threshold', 'result_window')

    edges = cv2.Canny(blurred_img, low_thresh, max_thresh)

cv2.destroyAllWindows()


# TODO: Test bilateral blurring
