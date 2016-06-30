import cv2
import numpy as np

from enum import Enum


class ThreshMethod(Enum):
    OTSU = 0
    FIXED = 1
    ADAPTIVE = 2


class SeparacionPalabras:
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


