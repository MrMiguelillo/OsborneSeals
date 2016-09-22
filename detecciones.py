import cv2
import numpy as np
import sys
import Separacion
import Filtros
import Umbralizaciones

umbralizaciones = Umbralizaciones.Umbralizaciones()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
file = sys.argv[1]
original = cv2.imread(file)

# Parametros modificables
minCol = 10
#minimo = [100, 100]

# Umbralizado de JSM
#img = umbralizaciones.umbralizar_imagen(file)
# Umbralizado nuestro
gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Eliminar posible borde negro
img = separar.borde(img)
# Calcular tamano de imagen
fil_px, col_px = img.shape
# Plantilla de pertenencia
img_plant = img < 255

# Separar columnas
hist_hor = separar.hor_hist(img_plant)
div = separar.columnas(hist_hor, minCol)
if np.isnan(div):
    num_paginas = 1
    tab = [0, col_px]
else:
    num_paginas = 2
    tab = [0, int(div), col_px]

# Separar filas
filas = []
num_filas = []
hist_ver_filtrado = []
minimo = np.zeros(num_paginas)
for x in range(0, num_paginas):
    # Histograma vertical
    hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x+1]])
    # Filtrado
    hist_ver_filtrado.append(filtro.mediana(hist_ver, 10))
    # Minimo
    minimo[x] = int(np.max(hist_ver_filtrado[x])/4)
    # Separar filas
    ini_filas, fin_filas = separar.filas(hist_ver_filtrado[x], minimo[x])

    num_filas.append(len(ini_filas))
    filas.append([ini_filas, fin_filas, tab[x], tab[x + 1]])

print(num_filas)