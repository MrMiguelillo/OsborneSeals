import cv2
import paths
import numpy as np
from matplotlib import pyplot as plt

from SellosHeuristica import LineSeparator as LiSe

path = paths.path_to_imgs
img = cv2.imread(path+'/1883-L119.M29/11/IMG_0001.png', cv2.IMREAD_GRAYSCALE)

otsu_thresh, bin_img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
bin_blurred = cv2.GaussianBlur(bin_img, (29, 29), 0)

hist = LiSe.horiz_proy(bin_blurred)
plt.plot(hist, 'b')

smooth_hist = LiSe.savitzky_golay(hist, 51, 3)
# plt.plot(smooth_hist, 'r')

mins = LiSe.find_min(smooth_hist)
min_x = []
min_y = []
for m in mins:
    min_x.append(m[0])
    min_y.append(m[1])
plt.plot(min_x, min_y, '.g')

is_out = LiSe.is_outlier(np.array(min_y))
outliers_x = []
outliers_y = []
for i, x in enumerate(is_out):
    if x:
        if hist[min_x[i]] > 0:
            outliers_x.append(min_x[i])
            outliers_y.append(min_y[i])
        else:
            is_out[i] = False
plt.plot(outliers_x, outliers_y, '.r')

# hist2 = LiSe.horiz_proy(bin_blurred)
# plt.plot(hist2, 'r')

for i, p in enumerate(min_x):
    if not is_out[i]:
        cv2.line(bin_img, (0, p), (3680, p), 1, 10)

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', bin_img*255)
# cv2.namedWindow('Imagen2', cv2.WINDOW_NORMAL)
# cv2.imshow('Imagen2', bin_blurred*255)
plt.show()
cv2.waitKey()
