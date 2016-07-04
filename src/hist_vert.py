import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros


# Comen
split = Separacion.Separacion()
filtro = Filtros.Filtros()

def separar_lineas():
    res_y = []
    return res_y


img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)

rows, cols = img.shape

sub_img = img[0:1791, 0:rows]
hist = split.vert_hist(sub_img)
plt.plot(hist, color='r')

smoothed_hist = filtro.filtro_mediana(hist, 10)
plt.plot(smoothed_hist, color='b')

plt.show()
