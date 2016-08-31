import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy
from PIL import Image, ImageDraw, ImageFont
from skimage import measure
from scipy import ndimage
import Separacion
import Filtros
import Umbralizaciones
import Umbralizacion

umbralizaciones = Umbralizaciones.Umbralizaciones()
umbralizacion = Umbralizacion.Umbralizacion()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Parámetros modificables
erosion = 5
num_paginas = 2
# Importar transcripción
transcripcion = '../../Osborne/RepoOsborne/documentos/1882-L123.M17/3/IMG_0004.txt'
legajo = '1882-L123.M17_3'
# Importar imagen original
file = '../../Osborne/RepoOsborne/documentos/1882-L123.M17/3/IMG_0004.png'

nombre = os.path.splitext(os.path.basename(file))[0]
path = os.path.dirname(file)
original = cv2.imread(file)
# Importar imagen binarizada
# Umbralizado de JSM
#img = umbralizar.umbralizar_imagen(file)
# Umbralizado nuestro
gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Calcular tamaño de imagen en centímetros
fil_px, col_px = img.shape

# Plantilla de pertenencia
img_plant = img < 255

print('Generar transcripción')
texto = []
with open(transcripcion) as inputfile:
    for line in inputfile:
        #texto.append(line.strip().split('\t'))
        texto.append(line.strip())

print("Separar columnas")
if num_paginas == 2:
    hist_hor = separar.hor_hist(img_plant)
    div = separar.columnas(hist_hor)
    tab = [0, div, col_px]
else:
    tab = [0, col_px]

print("Separar filas")
filas = []
num_filas = []
for x in range(0, num_paginas):
    # Histograma vertical
    hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x+1]])
    # Filtrado
    hist_ver_filtrado = filtro.mediana(hist_ver, 10)
    # Separar filas
    ini_filas, fin_filas = separar.filas(hist_ver_filtrado, 100)
    # Toma de datos
    num_filas.append(len(ini_filas))
    filas.append([ini_filas, fin_filas, tab[x], tab[x + 1]])

print("Encontrar palabras")
kernel = np.ones((5, 5), np.uint8)
img_ero = cv2.erode(img, kernel, iterations=erosion)
img_ero_bw = (img_ero < 1).astype('uint8')


num_palabras = []
palabras = []
for x in range(0, num_paginas):
    num_palabras_pagina = []
    palabras_pagina = []
    for y in range(0, num_filas[x]):
        # Seleccionar fila
        fila_ero_bw = img_ero_bw[filas[x][0][y]:filas[x][1][y], filas[x][2]:filas[x][3]]
        # Componentes conexas
        label_image = measure.label(fila_ero_bw)

        num_palabras_fila = 0
        palabras_fila = []

        for region in measure.regionprops(label_image):
            # skip small images
            if region.area < 1000:
                continue

            num_palabras_fila += 1
            minr, minc, maxr, maxc = region.bbox
            palabras_fila.append([minc + filas[x][2], minr + filas[x][0][y], maxc + filas[x][2], maxr + filas[x][0][y]])

        # Añadir número de palabras de una fila
        num_palabras_pagina.append(num_palabras_fila)

        # Ordenar palabras de una fila
        palabras_fila = sorted(palabras_fila, key=lambda coord: coord[0])
        # Añadir palabras de una fila
        palabras_pagina.append(palabras_fila)

    num_palabras.append(num_palabras_pagina)
    palabras.append(palabras_pagina)

l = 1
p = 1
id = 1
for x in range(0, num_paginas):
    for y in range(0, num_filas[x]):
        print("Página %d de %d - Fila %d de %d:   %d palabras" % (x + 1, num_paginas, y + 1, num_filas[x], num_palabras[x][y]))
        l += 1

        for z in range(0, num_palabras[x][y]):

            if texto[p - 1] != "xxx":

                recorte = original[palabras[x][y][z][1]:palabras[x][y][z][3], palabras[x][y][z][0]:palabras[x][y][z][2]]

                filestring = '../../Osborne/BdD/%s_%s_%d_%s.png' % (legajo, nombre, id, texto[p - 1])
                cv2.imwrite(filestring, recorte)

                filestring = '../../Osborne/BdD/%s_%s_%d_%s.txt' % (legajo, nombre, id, texto[p - 1])
                txt = open(filestring, 'w')
                txt.write('%s\n%s\n%s\n%d\n%d\n%d\n%d' % (legajo, nombre, texto[p - 1], palabras[x][y][z][0],
                                                          palabras[x][y][z][1], palabras[x][y][z][2],
                                                          palabras[x][y][z][3]))
                id += 1

            p += 1