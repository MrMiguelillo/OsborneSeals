import cv2
import numpy as np
import matplotlib.pyplot as plt
from functions import SeparacionPalabras
from functions import ThreshMethod

separar = SeparacionPalabras()
img = cv2.imread('D:\PycharmProjects\Lab_Osborne\imgs\IMG_0003.png', 0)
bin_img = separar.umbralizar_imagen(img, ThreshMethod.FIXED,180)

#hist_vert = histograma_vertical(img)
#plt.plot(hist_vert)
#plt.show()

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", bin_img)
cv2.waitKey()
