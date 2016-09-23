import cv2
import math
import numpy as np

DIM_VENTANA = 40
K_NIBLACK = -0.2
R_SAUVOLA = 128
K_SAUVOLA = 0.2
K_NICK = -0.1

class AlgoritmosLocales:
    def _calcular_desviacion_cuadrada(self, matriz, media):
        return np.sum(matriz.dot(matriz) - math.pow(media, 2))

    def _niblack(self, matriz, media, desviacion):
        umbral = media + (K_NIBLACK * desviacion)
        umbral = int(np.round(umbral, 0))
        return ((matriz >= umbral) * 255)

    def _sauvola(self, matriz, media, desviacion):
        umbral = media * (1 - (K_SAUVOLA *(1 - (desviacion / R_SAUVOLA))))
        umbral = int(np.round(umbral, 0))
        return ((matriz >= umbral) * 255)

    def _nick(self, matriz, media, desviacion_cuadrada):
        umbral = media + (K_NICK * desviacion_cuadrada)
        umbral = int(np.round(umbral, 0))
        return ((matriz >= umbral) * 255)

    def _generar_imagen_ampliada(self, imagen, filas, columnas):
        matriz_ampliada = np.zeros((filas + DIM_VENTANA, columnas + DIM_VENTANA), dtype=np.uint8)
        dimension = DIM_VENTANA - 10
        matriz_ampliada[0:10, 0:10] = imagen[0:10, 0:10]
        matriz_ampliada[10:filas+10, 0:10] = imagen[0:filas, 0:10]
        matriz_ampliada[filas+10:filas+DIM_VENTANA, 0:10] = imagen[filas-dimension:filas, 0:10]
        matriz_ampliada[0:10, 10:columnas+10] = imagen[0:10, 0:columnas]
        matriz_ampliada[10:filas+10, 10:columnas+10] = imagen[0:filas, 0:columnas]
        matriz_ampliada[filas+10:filas+DIM_VENTANA, 10:columnas+10] = imagen[filas-dimension:filas, 0:columnas]
        matriz_ampliada[0:10, columnas+10:columnas+DIM_VENTANA] = imagen[0:10, columnas-dimension:columnas]
        matriz_ampliada[10:filas+10, columnas+10:columnas+DIM_VENTANA] = imagen[0:filas, columnas-dimension:columnas]
        matriz_ampliada[filas+10:filas+DIM_VENTANA, columnas+10:columnas+DIM_VENTANA] = imagen[filas-dimension:filas, columnas-dimension:columnas]
        return matriz_ampliada

    def generar_matriz_local(self, imagen):
        dimension = DIM_VENTANA // 2
        nueva_dimension = dimension + 10
        filas, columnas = imagen.shape
        nuevas_filas = ((filas // dimension) + 1) * dimension
        nuevas_columnas = ((columnas // dimension) + 1) * dimension
        matriz_algo = np.zeros((nuevas_filas,nuevas_columnas), dtype=np.bool)
        matriz_ampliada = self._generar_imagen_ampliada(imagen, filas, columnas)
        for y in range(0, filas, dimension):
            for x in range(0, columnas, dimension):
                matriz_roi = matriz_ampliada[y:y+DIM_VENTANA, x:x+DIM_VENTANA]
                media, desviacion = cv2.meanStdDev(matriz_roi)
                desviacion_cuadrada = self._calcular_desviacion_cuadrada(matriz_roi, media)
                matriz_nueva = matriz_ampliada[y+10:y+nueva_dimension, x+10:x+nueva_dimension]
                matriz_niblack = self._niblack(matriz_nueva, media, desviacion)
                matriz_sauvola = self._sauvola(matriz_nueva, media, desviacion)
                matriz_nick = self._nick(matriz_nueva, media, desviacion_cuadrada)
                matriz_algo[y:y+dimension, x:x+dimension] = ((matriz_niblack + matriz_sauvola + matriz_nick) >= 510)
        matriz_algo = matriz_algo[0:filas, 0:columnas]
        return matriz_algo