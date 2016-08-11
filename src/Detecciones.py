import cv2
import numpy as np
from skimage import measure
from src import Separacion
from src import Filtros
from src import Umbralizaciones
from src import Umbralizacion

umbralizaciones = Umbralizaciones.Umbralizaciones()
umbralizacion = Umbralizacion.Umbralizacion()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()

class Detecciones:
    def detectar_filas(self, file, numPaginas):

        original = cv2.imread(file)

        # Umbralizado de JSM
        # img = umbralizar.umbralizar_imagen(file)
        # Umbralizado nuestro
        gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Calcular tamaño de imagen en pixeles
        fil_px, col_px = img.shape

        # Plantilla de pertenencia
        img_plant = img < 255

        # Separar columnas
        if numPaginas == 2:
            hist_hor = separar.hor_hist(img_plant)
            div = separar.columnas(hist_hor)
            tab = [0, div, col_px]
        else:
            tab = [0, col_px]

        # Separar filas
        filas = []
        num_filas = []
        for x in range(0, numPaginas):
            # Histograma vertical
            hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x + 1]])
            # Filtrado
            hist_ver_filtrado = filtro.mediana(hist_ver, 10)
            # Separar filas
            ini_filas, fin_filas = separar.filas(hist_ver_filtrado, 100)
            # Toma de datos
            num_filas.append(len(ini_filas))
            filas.append([ini_filas, fin_filas, tab[x], tab[x + 1]])

        # Encontrar palabras
        kernel = np.ones((5, 5), np.uint8)
        img_ero = cv2.erode(img, kernel, iterations=5)
        img_ero_bw = (img_ero < 1).astype('uint8')

        num_palabras = []
        palabras = []
        for x in range(0, numPaginas):
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
                    palabras_fila.append(
                        [minc + filas[x][2], minr + filas[x][0][y], maxc + filas[x][2], maxr + filas[x][0][y]])

                # Añadir número de palabras de una fila
                num_palabras_pagina.append(num_palabras_fila)
                # Ordenar palabras de una fila
                palabras_fila = sorted(palabras_fila, key=lambda coord: coord[0])
                # Añadir palabras de una fila
                palabras_pagina.append(palabras_fila)

            num_palabras.append(num_palabras_pagina)
            palabras.append(palabras_pagina)

        res = []
        for x in range(0, numPaginas):
            res_pagina = []
            for y in range(0, num_filas[x]):
                #print("Página %d de %d - Fila %d de %d:   %d palabras" % (x + 1, numPaginas, y + 1, num_filas[x], num_palabras[x][y]))

                B1 = -1
                for z in range(0, num_palabras[x][y]):

                    if palabras[x][y][z][2] > B1:
                        B1 = palabras[x][y][z][2]

                left = (palabras[x][y][0][0] / col_px) * 0.9 * 100
                top = (filas[x][0][y] / col_px) * 0.9 * 100

                width = ((B1 - palabras[x][y][0][0]) / col_px) * 0.9 * 100
                height = ((filas[x][1][y] - filas[x][0][y]) / col_px) * 0.9 * 100

                res_pagina.append([round(width, 2), round(height, 2), round(top, 2), round(left, 2)])

            res.append(res_pagina)

        return res