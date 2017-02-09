import numpy as np
import cv2.xfeatures2d as xf
import cv2

img1 = cv2.imread('C:/Users/usuario/Desktop/new_base/sello33.png', 0)    # trainImage
# img2 = cv2.imread('C:/Users/usuario/Desktop/documentos/1877-L119.M23_Tomas_Osborne_Bohl/'
#                   '1/1877-L119.M23_Tomas_Osborne_Bohl.I_1/IMG_0001.png', 0)  # queryImage

img2 = cv2.imread('C:/Users/usuario/Desktop/Document/2016_09_09/181/IMG_0001.png', 0)

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
        kp_matched.append(kp2[m.trainIdx])  # keypoints from query image stored for seal location calculation

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
# img3 = img2.copy()
# img3 = cv2.cvtColor(img3, cv2.COLOR_GRAY2BGR)
# for i in range(0, len(kp_matched)):
#     cv2.circle(img3, (int(kp_matched[i].pt[0]), int(kp_matched[i].pt[1])), 6, (0, 255, 0), thickness=-1)
#
# fils, cols = img2.shape
# for i in range(0, int(cols/100)):
#     cv2.line(img3, (100*i, 0), (100*i, fils), (255, 0, 50), thickness=5)
# for i in range(0, int(fils/100)):
#     cv2.line(img3, (0, 100*i), (cols, 100*i), (255, 0, 50), thickness=5)
# cv2.drawKeypoints(img2, kp_matched, img3, color=(0, 255, 0))
# print(len(kp_matched))


cv2.namedWindow('win', cv2.WINDOW_NORMAL)
cv2.imshow('win', img3)
cv2.waitKey()
cv2.destroyAllWindows()
