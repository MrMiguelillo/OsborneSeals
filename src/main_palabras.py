import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

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
num_filas = len(ini_filas)

print("Separar palabras")
res=[]
z=0
for x in range(0, num_filas):
    fila = img[ini_filas[x]:fin_filas[x], 0:colum]
    hist_fila = separar.hor_hist(fila)
    ini_palabras, fin_palabras = separar.palabras(hist_fila, 20, 80)

    num_palabras = len(ini_palabras)

    print("Fila %d de %d " % (x + 1, num_filas))

    for y in range(0, num_palabras):

        res.append([ini_palabras[y], ini_filas[x], fin_palabras[y], fin_filas[x]])

        palabra = img[ini_filas[x]:fin_filas[x], ini_palabras[y]:fin_palabras[y]]
        hist_palabra = separar.vert_hist(palabra)

        #res[z][1], res[z][3] = ajustar.palabras(hist_palabra)

        cv2.line(img, (res[z][0], res[z][1]), (res[z][0], res[z][3]), 100, 1)
        cv2.line(img, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
        cv2.line(img, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
        cv2.line(img, (res[z][0], res[z][3]), (res[z][2], res[z][3]), 100, 1)

        z = z + 1


print(res)
print("Resultados gráficos")
cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', img)
#cv2.imwrite('../salida_separadas.png', img)

plt.figure(1)
#plt.subplot(211)
plt.plot(hist_palabra)
#plt.plot(np.ones(tam)*100, ini_filas, 'ro')
#plt.plot(np.ones(tam)*100, fin_filas, 'bo')
plt.show()