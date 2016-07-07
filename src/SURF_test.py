import cv2.xfeatures2d as xf
import cv2


img = cv2.imread('../imgs/IMG_0003.png', 0)
# img = src[240:550, 700:1100]
surf = xf.SURF_create(500)

kp, des = surf.detectAndCompute(img, None)
print(len(kp))

# for i in range(1, len(kp)):


img2 = cv2.drawKeypoints(img, kp, None, (255, 0, 0), 4)
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow('result', img2)
cv2.waitKey()
