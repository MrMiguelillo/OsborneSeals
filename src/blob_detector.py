import cv2
import numpy as np

# Read image
original = cv2.imread("C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/sello1_trozo.png", cv2.IMREAD_GRAYSCALE)
im = cv2.resize(original, (0,0), None, 0.2, 0.2)
im = ((im > 200).astype('uint8'))*255

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0
params.maxThreshold = 100

# Filter by Area.
params.filterByArea = False
params.minArea = 1500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey()
