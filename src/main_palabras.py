import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen binarizada
img = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
# Importar imagen original
img2 = cv2.imread('../imgs/Narciso2.png', -1)

filas, colum = img.shape

print("Histograma vertical")
hist_ver = separar.vert_hist(img)

print("Filtrado del histograma vertical")
filtrado = filtro.mediana(hist_ver, 10)

print("Separar filas")
ini_filas, fin_filas = separar.filas(filtrado, 100)
num_filas = len(ini_filas)

# Separar palabras
res=[]
z=0
for y in range(0, num_filas):
    print("Separar palabras: Fila %d de %d " % (y + 1, num_filas))
    fila = img[ini_filas[y]:fin_filas[y], 0:colum]
    hist_fila = separar.hor_hist(fila)
    ini_palabras, fin_palabras = separar.palabras(hist_fila, 20, 80)

    num_palabras = len(ini_palabras)

    for x in range(0, num_palabras):

        res.append([ini_palabras[x], ini_filas[y], fin_palabras[x], fin_filas[y]])

        palabra = img[res[z][1]:res[z][3], res[z][0]:res[z][2]]

        # Separar palabras
        hist_palabra = separar.vert_hist(palabra)
        hist_palabra_filtrada = filtro.mediana(hist_palabra, 5)

        # Ajustar palabras
        ini, fin = separar.ajustar(hist_palabra_filtrada)
        res[z][1] = res[z][1] + ini
        res[z][3] = res[z][3] - fin

        # Dibujar rectángulos de palabras
        #cv2.line(img, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
        #cv2.line(img, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
        #cv2.line(img, (res[z][2], res[z][3]), (res[z][0], res[z][3]), 100, 1)
        #cv2.line(img, (res[z][0], res[z][3]), (res[z][0], res[z][1]), 100, 1)

        z += 1

# Ampliar palabras
z=1
for y in range(1, num_filas - 2):
    print("Ampliar palabras: Fila %d de %d" % (y, num_filas - 2))

    for x in range(0, num_palabras):
        # Ampliar palabras
        margen = 10
        ampliacion = img[(res[z][1] - margen):(res[z][3] + margen), res[z][0]:res[z][2]]
        hist_ampliado = separar.vert_hist(ampliacion)
        ini, fin = separar.ampliar(hist_ampliado, margen)
        res[z][1] = res[z][1] - margen + ini
        res[z][3] = res[z][3] + fin

        # Dibujar rectángulos de palabras
        cv2.line(img, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
        cv2.line(img, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
        cv2.line(img, (res[z][2], res[z][3]), (res[z][0], res[z][3]), 100, 1)
        cv2.line(img, (res[z][0], res[z][3]), (res[z][0], res[z][1]), 100, 1)

        z += 1


print("Resultados gráficos")
#cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
#cv2.imshow('result', img)
cv2.imwrite('../salida_pruebas.png', img)

#plt.figure(1)
#plt.subplot(211)
#plt.plot(hist_palabra)
#plt.plot(ini, hist_palabra[ini], 'ro')
#plt.plot(len(hist_palabra)-fin, hist_palabra[len(hist_palabra)-fin], 'bo')
#plt.show()