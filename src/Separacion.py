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

    # Entrada:  1. Histograma (ndarray)
    #           2. Ancho para convolucionar en el cálculo de la mediana (int)
    # Salida:   Histograma con la mediana calculada comparando cada punto con los n-vecinos, con n = ancho (list)
    def filtro_mediana(self, histograma, ancho):
        long = histograma.size
        filt_hist = []

        for i in range(0, long):
            if i < ancho:
                ordenado = sorted(histograma[0:i+ancho])
                rango = i + ancho
            elif i > (long - ancho):
                ordenado = sorted(histograma[i-ancho:long])
                rango = long - (i-ancho)
            else:
                ordenado = sorted(histograma[i-ancho:i + ancho])
                rango = 2*ancho
            valor = ordenado[int(rango/2)] # Ordenamos los valores y cogemos el de la mitad, redondeando la mitad hacia arriba
            filt_hist.append(valor)

        return filt_hist

    def filtro_media(self, datos, ancho):
        long = datos.size
        datos_suavizados = []
        for i in range(0, long):
            suma = 0
            rango = 0
            if i < ancho:
                rango = i + ancho
                for x in range(0, i + ancho):
                    suma += datos[i]
            elif i > (long - ancho):
                rango = long - (i - ancho)
                for x in range(i - ancho, long):
                    suma += datos[i]
            else:
                rango = 2 * ancho
                for x in range(i - ancho, i + ancho):
                    suma += datos[i]
            datos_suavizados.append(suma / rango)

        return datos_suavizados
