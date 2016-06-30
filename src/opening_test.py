import cv2
import numpy as np


img = cv2.imread('../met_2_vec_2_sig_0_thr_0_binImg.png', 0)
kernel = np.ones((9, 9), np.uint8)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', opening)
cv2.waitKey()
cv2.destroyAllWindows()

# APERTURA NO ELIMINA EL RUIDO
