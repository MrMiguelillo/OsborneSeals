import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
im = Image.open('../imgs/Narciso2.png')
ppi = im.info['dpi']
# Importar imagen binarizada
imagen = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
fil_px, col_px = imagen.shape
# Calcular tamaño de imagen en centímetros
fil = fil_px/(ppi[0]*0.39370)
col = col_px/(ppi[0]*0.39370)

print("El tamaño de la imagen es %.2f x %.2f centímetros" % (fil, col))

# Plantilla de pertenencia
img = imagen < 255

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
    fila = img[ini_filas[y]:fin_filas[y], 0:col_px]
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

        z += 1

total_palabras = len(res)
for z in range(0, total_palabras):
        cv2.line(imagen, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
        cv2.line(imagen, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
        cv2.line(imagen, (res[z][2], res[z][3]), (res[z][0], res[z][3]), 100, 1)
        cv2.line(imagen, (res[z][0], res[z][3]), (res[z][0], res[z][1]), 100, 1)

cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', imagen)

print("Resultados gráficos")
plt.figure(1)
plt.plot(filtrado)
plt.show()