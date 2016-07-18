import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

print("Importar imágenes")
# Importar imagen binarizada
img = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
# Importar imagen original
img2 = cv2.imread('../imgs/Narciso2.png', -1)

filas, colum = img.shape

print("Separar filas")
# Histograma vertical
hist_ver = separar.vert_hist(img)
# Filtrado
filtrado = filtro.mediana(hist_ver, 10)
# Separar filas
ini_filas, fin_filas = separar.filas(filtrado, 100)
num_filas = len(ini_filas)

print("Separar palabras")
num_palabras = []
res=[]
z=0
for y in range(0, num_filas):
    # Seleccionar fila
    fila = img[ini_filas[y]:fin_filas[y], 0:colum]
    # Histograma horizontal
    hist_fila = separar.hor_hist(fila)
    # Separar palabras
    ini_palabras, fin_palabras = separar.palabras(hist_fila, 20, 80)
    num_palabras.append(len(ini_palabras))

    print("Separar palabras: Fila %d de %d - Encontradas %d palabras " % (y + 1, num_filas, num_palabras[y]))

    for x in range(0, num_palabras[y]):

        res.append([ini_palabras[x], ini_filas[y], fin_palabras[x], fin_filas[y]])
        # Seleccionar palabra
        palabra = img[res[z][1]:res[z][3], res[z][0]:res[z][2]]
        # Histograma vertical
        hist_palabra = separar.vert_hist(palabra)
        # Filtrado
        #hist_palabra_filtrada = filtro.mediana(hist_palabra, 5)
        # Ajustar palabras
        ini, fin = separar.ajustar(hist_palabra)
        res[z][1] = res[z][1] + ini
        res[z][3] = res[z][3] - fin

        z += 1

# Ampliar palabras
z = num_palabras[0] - 1
for y in range(1, num_filas - 2):
    print("Ampliar palabras: Fila %d de %d" % (y, num_filas - 2))

    for x in range(0, num_palabras[y]):
        # Seleccionar palabra ampliada
        margen = 5
        ampliacion = img[(res[z][1] - margen):(res[z][3] + margen), res[z][0]:res[z][2]]
        # Histograma vertical
        hist_ampliado = separar.vert_hist(ampliacion)
        # Filtrado
        # hist_ampliado = filtro.mediana(hist_ampliado, 5)
        # Ampliar palabras
        ini, fin = separar.ampliar(hist_ampliado, margen)
        res[z][1] = res[z][1] - ini
        res[z][3] = res[z][3] + fin

        z += 1

total_palabras = len(res)
for z in range(0, total_palabras):
    cv2.line(img, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
    cv2.line(img, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
    cv2.line(img, (res[z][2], res[z][3]), (res[z][0], res[z][3]), 100, 1)
    cv2.line(img, (res[z][0], res[z][3]), (res[z][0], res[z][1]), 100, 1)

print("Resultados gráficos")
#cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
#cv2.imshow('result', img)
cv2.imwrite('../salida_ampliada_pruebas.png', img)

#plt.figure(1)
#plt.subplot(211)
#plt.plot(hist_palabra)
#plt.plot(ini, hist_palabra[ini], 'ro')
#plt.plot(len(hist_palabra)-fin, hist_palabra[len(hist_palabra)-fin], 'bo')
#plt.show()