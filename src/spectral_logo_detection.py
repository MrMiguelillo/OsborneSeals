import cv2
import numpy as np
from math import sqrt
from src import Umbralizacion

img = cv2.imread('C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/sello1_trozo.png', 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
g_img = cv2.GaussianBlur(gray, (0, 0), 6)

Y = abs(gray - g_img)
# Y = High pass filtered image

spectral_thresh = 30
chrom_thresh = 190

YCC_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
R = np.array(Y, dtype=float)
m, n = R.shape
Fl = img
for i in range(0, m):
    for j in range(0, n):
        #R[i, j] = sqrt(int(YCC_img[i][j][1]) * int(YCC_img[i][j][1]) + int(YCC_img[i][j][2]) * int(YCC_img[i][j][2]))
        if Y[i, j] >= spectral_thresh : #and R[i, j] <= chrom_thresh:
            Fl[i, j] = (255, 255, 255)


# umbralizar = Umbralizacion.Umbralizacion()
gray_Fl = 255*(cv2.cvtColor(Fl, cv2.COLOR_BGR2GRAY) < 230).astype('uint8')
#gray_Fl = cv2.cvtColor(Fl, cv2.COLOR_BGR2GRAY)
#se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
# mask = cv2.morphologyEx(gray_Fl, cv2.MORPH_CLOSE, se1)
#mask = cv2.morphologyEx(gray_Fl, cv2.MORPH_OPEN, se2)
#mask = np.dstack([mask, mask, mask]) / 255
#out = img * mask

#for i in range(0, m):
#    for j in range(0, n):
#        if gray_Fl[i,j] < 180:
#            gray_Fl[i,j] = 0
#        else:
#            gray_Fl[i, j] = 255

#filt_gray_Fl = cv2.medianBlur(gray_Fl, 3)
#filt_gray_Fl = cv2.GaussianBlur(filt_gray_Fl, (5, 5), 5)
# Fl = cv2.medianBlur(Fl, 5)
# Fl = cv2.GaussianBlur(Fl, (5,5), 6)
# bin_img = umbralizar.umbralizar_imagen(gray_Fl, 1, 180)

# Fl &= 240  # Set 4 less significant bits to 0
# hsv = cv2.cvtColor(Fl, cv2.COLOR_BGR2HSV)
# hist = cv2.calcHist([hsv], [0], None, [16], [0, 180])
# hist_B = cv2.calcHist([Fl], [0], None, [16], [0, 256])
# hist_G = cv2.calcHist([Fl], [1], None, [16], [0, 256])
# hist_R = cv2.calcHist([Fl], [2], None, [16], [0, 256])

# backProy_B = cv2.calcBackProject([Fl], [0], hist_B, [0, 256], 1)
# backProy_G = cv2.calcBackProject([Fl], [0], hist_G, [0, 256], 1)
# backProy_R = cv2.calcBackProject([Fl], [0], hist_R, [0, 256], 1)
# bckProy = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
# r,h,c,w = 250,90,400,125
# track_window = (c,r,w,h)
# term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
# ret, track_window = cv2.meanShift(bckProy, track_window, term_crit)

# x,y,w,h = track_window
# img2 = cv2.rectangle(Fl, (x,y), (x+w,y+h), (255, 0, 255),20)

#cv2.imwrite('sello1_Test.png', Fl)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', Fl)
cv2.waitKey()


# TODO: Spectral logo detection seems to be inconsistent for very dark seals.
