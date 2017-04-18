import cv2
import paths
import numpy as np
from matplotlib import pyplot as plt

from SellosHeuristica import LineSeparator as LiSe

path = paths.path_to_imgs
img = cv2.imread(path+'/1883-L119.M29/11/IMG_0001.png', cv2.IMREAD_GRAYSCALE)

otsu_thresh, bin_img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
bin_blurred = cv2.GaussianBlur(bin_img, (29, 29), 0)

hist = LiSe.horiz_proy(bin_img)
plt.plot(hist, 'b')

smooth_hist = LiSe.savitzky_golay(hist, 51, 3)
# plt.plot(smooth_hist, 'r')


mins = LiSe.find_min(smooth_hist)
min_x = []
min_y = []
min_sum = 0
for m in mins:
    min_sum += m[1]
    min_x.append(m[0])
    min_y.append(m[1])
average = min_sum / len(mins)
plt.plot(min_x, min_y, '.g')

# hist2 = LiSe.horiz_proy(bin_blurred)
# plt.plot(hist2, 'r')

plt.show()
# cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
# cv2.imshow('Imagen', bin_img*255)
# cv2.namedWindow('Imagen2', cv2.WINDOW_NORMAL)
# cv2.imshow('Imagen2', bin_blurred*255)
# cv2.waitKey()


# TODO: por aqí va la cosa
# TODO: usar http://stackoverflow.com/questions/4624970/finding-local-maxima-minima-with-numpy-in-a-1d-numpy-array
# TODO: Una vez encontrados los mínimos locales, dibujar línea para ver si se detectan bien las líneas
