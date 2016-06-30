import cv2
# import numpy as np

from src import Thresholding

separar = Thresholding()


def do_nothing(x):
    pass

img = cv2.imread('D:\PycharmProjects\Lab_Osborne\imgs\IMG_0003.png')
cv2.namedWindow('image_window', cv2.WINDOW_NORMAL)
cv2.namedWindow('control_window')

METHODLABEL = '1:OTSU-2:FIX-3:ADAP'

cv2.createTrackbar('Vecinity width', 'control_window', 0, 100, do_nothing)
cv2.createTrackbar('Vecinity height', 'control_window', 0, 100, do_nothing)
cv2.createTrackbar('Sigma X', 'control_window', 0, 100, do_nothing)
cv2.createTrackbar('Sigma Y', 'control_window', 0, 100, do_nothing)
cv2.createTrackbar(METHODLABEL, 'control_window', 0, 2, do_nothing)
cv2.createTrackbar('Bin Threshold', 'control_window', 0, 255, do_nothing)
cv2.createTrackbar('SWITCH', 'control_window', 0, 1, do_nothing)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
filtered_img = gray_img
bin_img = separar.thresholding_image(filtered_img, Thresholding.ThresholdMethod.fixed, 180)

while 1:
    cv2.imshow('image_window', bin_img)

    vec_w = cv2.getTrackbarPos('Vecinity width', 'control_window')
    vec_h = cv2.getTrackbarPos('Vecinity height', 'control_window')
    sigX = cv2.getTrackbarPos('Sigma X', 'control_window')
    sigY = cv2.getTrackbarPos('Sigma Y', 'control_window')
    method = cv2.getTrackbarPos(METHODLABEL, 'control_window')
    threshold = cv2.getTrackbarPos('Bin Threshold', 'control_window')
    switch = cv2.getTrackbarPos('SWITCH', 'control_window')

    method_enum = Thresholding.ThresholdMethod(method)

    kernel = (vec_w*2 + 1, vec_h*2 + 1)
    if switch == 1:
        filtered_img = cv2.GaussianBlur(gray_img, kernel, sigX)
        bin_img = separar.thresholding_image(filtered_img, method_enum, threshold)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    elif k == 9:  # TAB key
        filestring = 'met_%d_vec_%d_sig_%d_thr_%d_binImg.png' % (method, vec_w, sigX, threshold)
        cv2.imwrite(filestring, bin_img)

cv2.destroyAllWindows()
