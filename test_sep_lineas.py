import cv2
import paths
import numpy as np
from matplotlib import pyplot as plt

from SellosHeuristica import LineSeparator as LiSe

path = paths.path_to_imgs
img = cv2.imread(path+'/2016_09_09/181/IMG_0002.png', cv2.IMREAD_GRAYSCALE)

otsu_thresh, bin_img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
bin_blurred = cv2.GaussianBlur(bin_img, (11, 11), 0)

if LiSe.has_two_pages(bin_blurred):
    ranges = ((0                            , int(bin_blurred.shape[1] / 2)),
              (int(bin_blurred.shape[1] / 2), bin_blurred.shape[1]))
else:
    ranges = ((0, bin_blurred.shape[1]),)

for rng in ranges:
    hist = LiSe.proyect(bin_blurred[:, rng[0]:rng[1]], axis=LiSe.axis["horizontal"])
    # plt.plot(hist, 'r')

    smooth_hist = LiSe.savitzky_golay(hist, 51, 3)
    plt.plot(smooth_hist, 'b')

    mins = LiSe.find_min(smooth_hist)
    min_x = [i[0] for i in mins]
    min_y = [i[1] for i in mins]
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

    for i, xs in enumerate(min_x):
        if not is_out[i]:
            cv2.line(bin_blurred, (rng[0], xs), (rng[1], xs), 1, 10)

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', bin_blurred*255)
plt.show()
cv2.waitKey()
