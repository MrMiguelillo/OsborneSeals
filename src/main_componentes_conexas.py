import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
original = Image.open('../imgs/Narciso2.png')
ppi = original.info['dpi']

# Importar imagen binarizada
imagen = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
fil_px, col_px = imagen.shape

# Calcular tamaño de imagen en centímetros
fil_cm = fil_px/(ppi[0]*0.39370)
col_cm = col_px/(ppi[0]*0.39370)

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
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(imagen,kernel,iterations = 2)

ero = erosion < 255
num_palabras = []
res=[]
z=0
for y in range(0, num_filas):
    # Seleccionar fila
    fila = ero[ini_filas[y]:fin_filas[y], 0:col_px]
    # Histograma horizontal
    hist_fila = separar.hor_hist(fila)
    # Separar palabras
    minimo_hueco = 5
    minimo_palabra = 20
    ini_palabras, fin_palabras = separar.palabras(hist_fila, minimo_hueco, minimo_palabra)
    num_palabras.append(len(ini_palabras))

    print("Separar palabras: Fila %d de %d - Encontradas %d palabras " % (y + 1, num_filas, num_palabras[y]))

    for x in range(0, num_palabras[y]):

        res.append([ini_palabras[x], ini_filas[y], fin_palabras[x], fin_filas[y]])
        # Seleccionar palabra
        palabra = ero[res[z][1]:res[z][3], res[z][0]:res[z][2]]
        # Histograma vertical
        hist_palabra = separar.vert_hist(palabra)
        # Filtrado
        # hist_palabra_filtrada = filtro.mediana(hist_palabra, 5)
        # Ajustar palabras
        ini, fin = separar.ajustar(hist_palabra)
        res[z][1] = res[z][1] + ini
        res[z][3] = res[z][3] - fin

        z += 1

total_palabras = len(res)
for z in range(0, total_palabras):
        cv2.line(imagen, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
        cv2.line(imagen, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
        cv2.line(imagen, (res[z][2], res[z][3]), (res[z][0], res[z][3]), 100, 1)
        cv2.line(imagen, (res[z][0], res[z][3]), (res[z][0], res[z][1]), 100, 1)


print("Resultados gráficos")
#cv2.imwrite('../prueba_compconex.png', img)
plt.figure(1)
plt.subplots_adjust(.01,.01,.99,.99)
plt.set_cmap("gray")
plt.imshow(imagen)
plt.show()
#plt.figure(2)
#plt.plot(filtrado)
#plt.show()