import numpy as np
import cv2.xfeatures2d as xf
import cv2

img1 = cv2.imread('C:/Users/usuario/Desktop/Base_sellos/sello6.png', 0)    # trainImage
img2 = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)  # queryImage

# Initiate SURF detector
sift = xf.SURF_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

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
        kp_matched.append(kp2[m.queryIdx])  # keypoints from query image stored for seal location calculation

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=0)

# kp_x = []
# kp_y = []
# for i in range(len(kp_matched)):
#     kp_x.append(kp_matched[i].pt[0])
#     kp_y.append(kp_matched[i].pt[1])
# max_x = np.amax(kp_x)
# min_x = np.amin(kp_x)
# max_y = np.amax(kp_y)
# min_y = np.amin(kp_y)

# cv2.rectangle(img2, (int(min_x),int(min_y)), (int(max_x),int(max_y)), 150, 5)

img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
print(len(kp_matched))


cv2.namedWindow('win', cv2.WINDOW_NORMAL)
cv2.imshow('win', img3)
cv2.waitKey()
cv2.destroyAllWindows()
