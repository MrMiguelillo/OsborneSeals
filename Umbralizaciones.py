import AlgoritmosLocales
import cv2
import numpy as np

DIMENSION_VENTANA = 40

class Umbralizaciones:
    def _leer_imagen(self, fichero):
        imagen = cv2.imread(fichero, 0)
        return imagen

    def _calcular_histograma(self, imagen):
        canales = [0]
        dimension = [256]
        rango = [0, 256]
        histograma = cv2.calcHist([imagen], canales, None, dimension, rango)
        return histograma

    def _calcular_media(self, histograma, inicial, final):
        media = 0
        total_pixeles = 0
        for i in range(inicial, final):
            media = media + (histograma[i] * i)
            total_pixeles = total_pixeles + histograma[i]
        media = media / total_pixeles
        return media

    def _calcular_dmin(self, histograma, umbral):
        izq = self._calcular_media(histograma, 0, umbral + 1)
        der = self._calcular_media(histograma, umbral + 1, 256)
        dmin1 = round(umbral - izq[0], 0)
        dmin2 = round(der[0] - umbral, 0)
        dmin = min(dmin1, dmin2)
        return dmin

    def _calcular_umbrales(self, umbral, dmin):
        umbral1 = umbral - (dmin / 2)
        umbral2 = umbral + (dmin / 2)
        umbrales = (umbral1, umbral2)
        return umbrales

    def _realizar_umbralizacion_local(self, imagen, umbrales):
        locales = AlgoritmosLocales.AlgoritmosLocales()
        umbral1, umbral2 = umbrales
        mascara_umbral_1 = imagen < umbral1
        mascara_umbral_2 = imagen > umbral2
        matriz_local = locales.generar_matriz_local(imagen)
        matriz_umbralizada = np.logical_or(matriz_local, mascara_umbral_2)
        matriz_umbralizada = np.logical_and(np.logical_not(mascara_umbral_1),matriz_umbralizada)
        matriz_umbralizada = (matriz_umbralizada * 255).astype(np.uint8)
        return matriz_umbralizada

    def umbralizar_imagen(self, fichero):
        imagen = self._leer_imagen(fichero)
        ret, th = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        histograma = self._calcular_histograma(imagen)
        dmin = self._calcular_dmin(histograma, int(ret))
        umbrales = self._calcular_umbrales(ret, dmin)
        imagen_umbralizada = self._realizar_umbralizacion_local(imagen, umbrales)
        return imagen_umbralizada