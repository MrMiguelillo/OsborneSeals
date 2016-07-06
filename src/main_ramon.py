import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtros = Filtros.Filtros()

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
filtrado1 = filtros.mediana(hist_ver1, 10)
filtrado2 = filtros.mediana(hist_ver2, 10)

print("Separar filas")
inicios1,finales1 = separar.filas(filtrado1, 20)
inicios2,finales2 = separar.filas(filtrado2, 100)
tam1 = len(inicios1)
tam2 = len(inicios2)

for x in range(0,tam1):
    cv2.line(img, (0, inicios1[x]), (div, inicios1[x]), 100, 5)
    cv2.line(img, (0, finales1[x]), (div, finales1[x]), 100, 5)
for x in range(0, tam2):
    cv2.line(img, (div, inicios2[x]), (colum, inicios2[x]), 100, 5)
    cv2.line(img, (div, finales2[x]), (colum, finales2[x]), 100, 5)

print("Separar palabras")

img2 = cv2.imread('../met_0_vec_2_sig_-1_thr_0_binImg.png', 0)

for x in range(0,tam2):
    fila = img2[inicios2[x]:finales2[x],div:colum]
    hist_fila = separar.hor_hist(fila)

    ini_palabra,fin_palabra = separar.palabras(hist_fila,10)
    tam_palabra = len(ini_palabra)

    for y in range(0,tam_palabra):
        cv2.line(img, (div+ini_palabra[y],inicios2[x]), (div+ini_palabra[y],finales2[x]), 100, 5)
        cv2.line(img, (div+fin_palabra[y],inicios2[x]), (div+fin_palabra[y],finales2[x]), 100, 5)


cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', img)

print("Resultados gráficos")
plt.figure(1)
plt.subplot(211)
plt.plot(hist_fila)
plt.subplot(212)
plt.plot(filtrado2)
plt.plot(inicios2,np.ones(tam2)*100,'ro')
plt.plot(finales2,np.ones(tam2)*101,'bo')
plt.show()

#cv2.waitKey()
#cv2.destroyAllWindows()