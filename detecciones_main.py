import cv2
import numpy as np
import os
import sys
import Separacion
import Filtros
import Umbralizaciones

umbralizaciones = Umbralizaciones.Umbralizaciones()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
file = 'imgs/0003_sin_escudo.png'
#file = 'imgs/Narciso2.png'
#file = '../../Osborne/RepoOsborne/documentos/1883-L119.M29/2/IMG_0001.png'
#file = sys.argv[1]

# Parámetros modificables
erosion = 5

nombre = os.path.splitext(os.path.basename(file))[0]
path = os.path.dirname(file)
original = cv2.imread(file)

# Umbralizado de JSM
#img = umbralizaciones.umbralizar_imagen(file)
# Umbralizado nuestro
gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
fil_px, col_px = img.shape
# Plantilla de pertenencia
img_plant = img < 255

# Separar columnas
hist_hor = separar.hor_hist(img_plant)
div = separar.columnas(hist_hor)
if np.isnan(div):
    num_paginas = 1
    tab = [0, col_px]
else:
    num_paginas = 2
    tab = [0, int(div), col_px]

# Separar filas
kernel = np.ones((5, 5), np.uint8)
img_dil = cv2.dilate(img, kernel, iterations = 1)
img_dil_plant = img_dil < 255

filas = []
num_filas = []
hist_ver_filtrado = []
for x in range(0, num_paginas):
    # Histograma vertical
    hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x+1]])
    # Filtrado
    hist_ver_filtrado.append(filtro.mediana(hist_ver, 10))

    # Elegir mínimo
    #minimo = int(np.max(hist_ver_filtrado[x])/3)
    minimo = 100

    # Separar filas
    ini_filas, fin_filas = separar.filas(hist_ver_filtrado[x], minimo)
    # Toma de datos
    num_filas.append(len(ini_filas))
    filas.append([ini_filas, fin_filas, tab[x], tab[x + 1]])

print(num_filas)


# Generar XML
filestring_xml = '%s/%s.html' % (path, nombre)
xml = open(filestring_xml, 'w')

cabecera = """<!DOCTYPE html>
<html>
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <head>
  <link rel="stylesheet" type="text/css" href="main.css">
 </head>
 <body>
"""
xml.write(cabecera)
xml.write('<img src="%s.png" alt="Documento Osborne" style="position: absolute; width:90%%"></img>\n' % (nombre))

p = 1
for x in range(0, num_paginas):
    for y in range(0, num_filas[x]):

        left = tab[x] / col_px * 0.9 * 100
        top = (filas[x][0][y] / col_px) * 0.9 * 100

        width = ((tab[x + 1] - tab[x]) / col_px) * 0.9 * 100
        height = ((filas[x][1][y] - filas[x][0][y]) / col_px) * 0.9 * 100

        xml.write('<canvas  title = "%d" id = "%d" style = "position: absolute;  width:%.2fvw; height:%.2fvw;'
        'top:%.2fvw;  left:%.2fvw; border:1px solid #0000FF;"></canvas>\n' % (p, p, width, height, top, left))

        p += 1

xml.write('</body>\n</html>\n')
xml.close()