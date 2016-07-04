import cv2
import numpy as np


class Filtros:
    # Entrada:  1. Histograma
    #           2. Ancho para convolucionar en el cálculo de la mediana
    # Salida:   Histograma con la mediana calculada comparando cada punto con los n-vecinos, con n = ancho
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