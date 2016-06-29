import cv2
import numpy as np

from enum import Enum


class ThreshMethod(Enum):
    OTSU = 0
    FIXED = 1
    ADAPTIVE = 2


class SeparacionPalabras:
    @staticmethod
    def umbralizar_imagen(self, gray_image, t_method, thresh=180):
        umb_img = gray_image
        if t_method == ThreshMethod.OTSU:
            ret, umb_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        elif t_method == ThreshMethod.FIXED:
            ret, umb_img = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)

        elif t_method == ThreshMethod.ADAPTIVE:
            umb_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        return umb_img

    @staticmethod
    def histograma_vertical(self, img):
        rows, cols = img.shape
        hist = np.zeros(rows)
        suma = 0

        for x in range(0, rows):
            for y in range(0, cols):
                if img[x, y] == 0:
                    suma += 1
            hist[x] = suma
            suma = 0

        return hist

    @staticmethod
    def histograma_horizontal(self, img):
        rows, cols = img.shape
        hist = np.zeros(cols)
        suma = 0

        for y in range(0, cols):
            for x in range(0, rows):
                if img[x, y] == 0:
                    suma += 1
            hist[y] = suma
            suma = 0

        return hist


