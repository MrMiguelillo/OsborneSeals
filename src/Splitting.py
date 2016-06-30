import cv2
import numpy as np


class Splitting:
    def vert_hist(self, img):
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

    def hor_hist(self, img):
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
