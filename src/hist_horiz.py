import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion

separar = Separacion.Separacion()

img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)

hist = separar.hor_hist(img)
plt.plot(hist)
plt.show()

divx = separar.separar_columnas(hist)
print(divx)

cv2.line(img, (divx, 0), (divx, 10000), 100, 5)
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow('result', img)

cv2.waitKey()
cv2.destroyAllWindows()

