import numpy as np
import cv2
import cv2.xfeatures2d as xf
import src.EvidenceMatrix as em

img1 = cv2.imread('C:/Users/usuario/Desktop/Base_sellos/sello6.png', 0)    # queryImage
img2 = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)  # trainImage


# --------------- DETECTION ---------------


# Initiate SURF detector
surf = xf.SURF_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = surf.detectAndCompute(img1, None)
kp2, des2 = surf.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in range(len(matches))]

kp_matched = []

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.9*n.distance:
        matchesMask[i] = [1, 0]
        kp_matched.append(kp2[m.trainIdx])  # keypoints from train image stored for seal location calculation

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=0)


img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)


cv2.namedWindow('win', cv2.WINDOW_NORMAL)
cv2.imshow('win', img3)


# --------------- OUTLIERS ELIMINATION ---------------

seal_locator = em.SealLocator(img2)
seal_locator.calc_occurrences(kp_matched)
y, x = seal_locator.calc_position()
num_div = seal_locator.DIVISION_SIZE

kpMask = [1 for i in range(len(kp_matched))]

img4 = img2.copy()
img4 = cv2.cvtColor(img4, cv2.COLOR_GRAY2BGR)

cv2.circle(img4, (x*num_div, y*num_div), 15, (255, 0, 255), thickness=-1)

cv2.namedWindow('win2', cv2.WINDOW_NORMAL)
cv2.imshow('win2', img4)
cv2.waitKey()
cv2.destroyAllWindows()

