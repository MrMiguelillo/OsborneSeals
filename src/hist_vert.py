import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion

# Comen
split = Separacion.Separacion()


def separar_lineas():
    res_y = []
    return res_y


def average_smoothing(data, width):
    length = data.size
    smoothed_data = []
    for i in range(0, length):
        suma = 0
        if i < width:
            for x in range(0, i+width):
                suma += data[i]
        if i > (length - width):
            for x in range(i-width, length):
                suma += data[i]
        else:
            for x in range(i-width, i+width):
                suma += data[i]
        smoothed_data.append(suma / (2*width + 1))

    return smoothed_data

img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)

rows, cols = img.shape

sub_img = img[0:1791, 0:rows]
hist = split.vert_hist(sub_img)
plt.plot(hist, color='r')

smoothed_hist = average_smoothing(hist, 100)
plt.plot(smoothed_hist, color='b')

plt.show()
