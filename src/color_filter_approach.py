import cv2
import numpy as np


def do_nothing(x):
    pass

img = cv2.imread('../imgs/IMG_0003.png', cv2.IMREAD_COLOR)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.namedWindow('H Filter', cv2.WINDOW_NORMAL)
cv2.namedWindow('S Filter', cv2.WINDOW_NORMAL)
cv2.namedWindow('V Filter', cv2.WINDOW_NORMAL)
cv2.namedWindow('control_window')

cv2.createTrackbar('H sup', 'control_window', 0, 180, do_nothing)
cv2.createTrackbar('H inf', 'control_window', 0, 180, do_nothing)
cv2.createTrackbar('S sup', 'control_window', 0, 255, do_nothing)
cv2.createTrackbar('S inf', 'control_window', 0, 255, do_nothing)
cv2.createTrackbar('V', 'control_window', 0, 255, do_nothing)

while 1:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    H_sup = cv2.getTrackbarPos('H sup', 'control_window')
    H_inf = cv2.getTrackbarPos('H inf', 'control_window')
    S_sup = cv2.getTrackbarPos('S sup', 'control_window')
    S_inf = cv2.getTrackbarPos('S inf', 'control_window')
    V = cv2.getTrackbarPos('V', 'control_window')

    # h_filtered = np.logical_and((hsv_img[:, :, 0] < H_sup), (hsv_img[:, :, 0] > H_inf)).astype(np.uint8) * 255
    # s_filtered = np.logical_and((hsv_img[:, :, 1] < S_sup), (hsv_img[:, :, 1] > S_inf)).astype(np.uint8) * 255
    # v_filtered = (hsv_img[:, :, 2] < V).astype(np.uint8) * 255
    #
    # cv2.imshow('H Filter', h_filtered)
    # cv2.imshow('S Filter', s_filtered)
    # cv2.imshow('V Filter', v_filtered)

    filt = np.logical_and(hsv_img[:, :, 0] < H_sup, hsv_img[:, :, 0] > H_inf).astype(np.uint8) * 255