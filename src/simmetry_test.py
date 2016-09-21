import cv2
import numpy as np


# 1. crop half doc_img
# 2. flip it and put it on top of the other half
# 3. substract it and calc area
# 4. compare it with the original area of that half

img = cv2.imread('dilated_seal.png', 0)
fil, col = img.shape

img_left = img[0:fil, 0:col/2]
img_right = img[0:fil, col/2:col]
flip_img_left = cv2.flip(img_left, 1)  # 1 means y axis
subtracted_img = abs(flip_img_left - img_right)

sub_area = np.sum(subtracted_img)
ref_area = (np.sum(img_left, dtype=np.float64) + np.sum(img_right, dtype=np.float64)) / 2.0

ratio = sub_area / ref_area

print(ratio)
