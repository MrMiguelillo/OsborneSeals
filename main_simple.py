import cv2
import numpy as np
import matplotlib.pyplot as plt
import Separacion
import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

print("Importar imagen umbralizada")
img = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)

filas, colum = img.shape

print("Importar imagen original")
img2 = cv2.imread('../imgs/Narciso2.png', -1)

print("Histograma vertical")
hist_ver = separar.vert_hist(img)

print("Filtrado")
filtrado = filtro.mediana(hist_ver, 10)

print("Separar filas")
ini_filas, fin_filas = separar.filas(filtrado, 100)
tam = len(ini_filas)

for x in range(0,tam):
    cv2.line(img, (0, ini_filas[x]), (colum, ini_filas[x]), 100, 5)
    cv2.line(img, (0, fin_filas[x]), (colum, fin_filas[x]), 100, 5)

print("Separar palabras")
for x in range(0,tam):
    fila = img[ini_filas[x]:fin_filas[x], 0:colum]
    hist_fila = separar.hor_hist(fila)
    ini_palabras, fin_palabras = separar.palabras(hist_fila, 20, 80)

    tam_palabra = len(ini_palabras)
    for y in range(0,tam_palabra):
        cv2.line(img, (ini_palabras[y], ini_filas[x]), (ini_palabras[y], fin_filas[x]), 100, 3)
        cv2.line(img, (fin_palabras[y], ini_filas[x]), (fin_palabras[y], fin_filas[x]), 100, 3)

#cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
#cv2.imshow('result', img)
#cv2.imwrite('../salida1_umbralizada.png', img)

print("Resultados gráficos")
plt.figure(1)
#plt.subplot(211)
plt.plot(filtrado, range(0, filas))
plt.plot(np.ones(tam)*100, ini_filas, 'ro')
plt.plot(np.ones(tam)*100, fin_filas, 'bo')
plt.show()
