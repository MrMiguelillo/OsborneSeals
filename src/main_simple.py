import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

#img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)
img = cv2.imread('../met_1_vec_0_sig_0_thr_143_binImg.png', 0)
img2 = cv2.imread('../imgs/Narciso2.png', -1)

filas, colum = img.shape

print("Histograma horizontal")
#hist_hor = separar.hor_hist(img)

print("Histograma vertical")
hist_ver = separar.vert_hist(img)

print("Filtrado")
filtrado = filtro.mediana(hist_ver, 10)

print("Separar filas")
ini_filas, fin_filas = separar.filas(filtrado, 20)
tam = len(ini_filas)

for x in range(0,tam):
    cv2.line(img2, (0, ini_filas[x]), (colum, ini_filas[x]), 100, 1)
    cv2.line(img2, (0, fin_filas[x]), (colum, fin_filas[x]), 100, 1)

print("Separar palabras")
for x in range(0,tam):
    fila = img[ini_filas[x]:fin_filas[x], 0:colum]
    hist_fila = separar.hor_hist(fila)
    ini_palabra,fin_palabra = separar.palabras(hist_fila,20,80)

    tam_palabra = len(ini_palabra)
    for y in range(0,tam_palabra):
        cv2.line(img2, (ini_palabra[y], ini_filas[x]), (ini_palabra[y], fin_filas[x]), 100, 1)
        cv2.line(img2, (fin_palabra[y], ini_filas[x]), (fin_palabra[y], fin_filas[x]), 100, 1)


#cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
#cv2.imshow('result', img)
cv2.imwrite('../salida1.png', img2)

print("Resultados gráficos")
plt.figure(1)
#plt.subplot(211)
plt.plot(hist_ver)
#plt.plot(ini_palabra, np.zeros(tam_palabra), 'ro')
#plt.plot(fin_palabra, np.zeros(tam_palabra), 'bo')
plt.show()