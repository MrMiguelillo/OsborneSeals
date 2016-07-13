import cv2
from math import sqrt

img = cv2.imread('C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/tomas_osborne1.png', 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
g_img = cv2.GaussianBlur(gray, (0, 0), 6)

Y = abs(gray - g_img)
fil, col = Y.size()
# Y = High pass filtered image

spectral_thresh = 35
chrom_thresh = 190

YCC_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
# TODO: Crear R elemento a elemento
R = sqrt(YCC_img[1]*YCC_img[1] + YCC_img[2]*YCC_img[2])

Fl = Y
for i in range(0, fil):
    for j in range(0,col):
        if Y[i,j] < spectral_thresh or R[i,j] > chrom_thresh:
            Fl[i, j] = img[i,j]
        else:
            Fl[i, j] = 255

