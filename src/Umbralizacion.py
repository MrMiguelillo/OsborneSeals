import cv2
from enum import Enum


class ThresholdMethod(Enum):
    otsu = 0
    fixed = 1
    adaptive = 2


class Thresholding:
    def thresholding_image(self, gray_image, threshold_method, threshold=180):
        threshold_image = gray_image
        if threshold_method == ThresholdMethod.otsu:
            ret, threshold_image  = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        elif threshold_method == ThresholdMethod.fixed:
            ret, threshold_image  = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

        elif threshold_method == ThresholdMethod.adaptive:
            threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        return threshold_image