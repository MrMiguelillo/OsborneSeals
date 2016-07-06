import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)
filas, colum = img.shape

print("Histograma horizontal")
hist_hor = separar.hor_hist(img)


print("Separar columnas")
div = separar.columnas(hist_hor)
cv2.line(img, (div,0), (div, filas), 100, 5)


print("Histograma vertical")
sub_img1 = img[0:filas,0:div]
sub_img2 = img[0:filas,div:colum]
hist_ver1 = separar.vert_hist(sub_img1)
hist_ver2 = separar.vert_hist(sub_img2)


print("Filtrado")
filtrado1 = filtro.mediana(hist_ver1, 10)
filtrado2 = filtro.mediana(hist_ver2, 10)


print("Separar filas")
ini_filas1, fin_filas1 = separar.filas(filtrado1, 20)
ini_filas2, fin_filas2 = separar.filas(filtrado2, 100)
tam1 = len(ini_filas1)
tam2 = len(ini_filas2)

for x in range(0,tam1):
    cv2.line(img, (0, ini_filas1[x]), (div, ini_filas1[x]), 100, 5)
    cv2.line(img, (0, fin_filas1[x]), (div, fin_filas1[x]), 100, 5)
for x in range(0, tam2):
    cv2.line(img, (div, ini_filas2[x]), (colum, ini_filas2[x]), 100, 5)
    cv2.line(img, (div, fin_filas2[x]), (colum, fin_filas2[x]), 100, 5)


print("Separar palabras")
for x in range(0,tam2):
    fila = img[ini_filas2[x]:fin_filas2[x], div:colum]
    hist_fila = separar.hor_hist(fila)
    ini_palabra,fin_palabra = separar.palabras(hist_fila,20,80)

    tam_palabra = len(ini_palabra)
    for y in range(0,tam_palabra):
        cv2.line(img, (div + ini_palabra[y], ini_filas2[x]), (div + ini_palabra[y], fin_filas2[x]), 100, 5)
        cv2.line(img, (div + fin_palabra[y], ini_filas2[x]), (div + fin_palabra[y], fin_filas2[x]), 100, 5)

cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', img)


print("Resultados gráficos")
plt.figure(1)
#plt.subplot(211)
plt.plot(hist_fila)
plt.plot(ini_palabra, np.zeros(tam_palabra), 'ro')
plt.plot(fin_palabra, np.zeros(tam_palabra), 'bo')
plt.show()

#cv2.waitKey()
#cv2.destroyAllWindows()