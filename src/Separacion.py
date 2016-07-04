import cv2
import numpy as np


class Separacion:
    def vert_hist(self, img):
        filas, colum = img.shape
        hist = np.zeros(filas)
        suma = 0

        for x in range(0, filas):
            for y in range(0, colum):
                if img[x, y] == 0:
                    suma += 1
            hist[x] = suma
            suma = 0
        return hist

    def hor_hist(self, img):
        filas, colum = img.shape
        hist = np.zeros(colum)
        suma = 0

        for y in range(0, colum):
            for x in range(0, filas):
                if img[x, y] == 0:
                    suma += 1
            hist[y] = suma
            suma = 0
        return hist

    # Entrada: Histograma horizontal
    # Salida: Tuplet: (Coordenada horizontal de la división de la página, longitud de la racha máxima de mínimos en el
    #       histograma). El segundo valor del tuplet se utiliza para saber si el documento tiene una columna de texto
    #       únicamente y no necesita ser dividido
    def columnas(self, histograma):
        long = histograma.size
        min_i = round(long / 3, 0)
        max_i = round(2 * long / 3, 0)
        suma = 0
        hueco = 0
        tam_hueco = 0
        min_x_actual = float('Inf')
        max_x_actual = 0
        min_x_hueco = float('Inf')
        max_x_hueco = 0

        for x in range(int(min_i), int(max_i)):
            if histograma[x] <= 10:
                suma += 1
                if min_x_actual == float('Inf'):
                    min_x_actual = x
            else:
                hueco = suma
                suma = 0
                max_x_actual = x

            if hueco > tam_hueco:
                tam_hueco = hueco
                min_x_hueco = min_x_actual
                max_x_hueco = max_x_actual

        res_x = round((max_x_hueco - min_x_hueco) / 2, 0) + min_x_hueco
        return int(res_x)


    def filas(self, histograma):
        long = histograma.size
        ini = []
        fin = []
        res = []
        for x in range(0, long-1):
            if (histograma[x] == 0.) & (histograma[x + 1] != 0.):
                ini.append(x + 1)

            if (histograma[x] != 0.) & (histograma[x + 1] == 0.):
                fin.append(x)

        tam=len(ini)
        res.append(ini[0]/2)
        for x in range(0, tam - 1):
            res.append(int((fin[x] - ini[x + 1]) / 2 + ini[x + 1]))

        return res


