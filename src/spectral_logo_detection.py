import cv2
import numpy as np
from math import sqrt

img = cv2.imread('C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/tomas_osborne1.png', 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
g_img = cv2.GaussianBlur(gray, (0, 0), 6)

Y = abs(gray - g_img)
fil, col = Y.shape
# Y = High pass filtered image

spectral_thresh = 35
chrom_thresh = 190

YCC_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
R = np.array(Y, dtype=float)
# TODO: Crear R elemento a elemento
m, n = R.shape
for i in range(0, m):
    for j in range(0, n):
        R[i, j] = sqrt(int(YCC_img[i][j][1]) * int(YCC_img[i][j][1]) + int(YCC_img[i][j][2]) * int(YCC_img[i][j][2]))


Fl = img
for i in range(0, fil):
    for j in range(0, col):
        if Y[i, j] >= spectral_thresh and R[i, j] <= chrom_thresh:
            Fl[i, j] = (255, 0, 255)

Fl = cv2.medianBlur(Fl, 5)
Fl = cv2.GaussianBlur(Fl, (5,5), 6)


cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', Fl)
cv2.waitKey()
