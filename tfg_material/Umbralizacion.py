import cv2
from enum import Enum


class Umbralizacion:
    class MetodoUmbralizado(Enum):
        otsu = 0
        fixed = 1
        adaptive = 2

    @staticmethod
    def umbralizar_imagen(imagen_grises, metodo_umbralizar, umbral=180):
        imagen_umbralizada = imagen_grises

        if metodo_umbralizar == Umbralizacion.MetodoUmbralizado.otsu:
            ret, imagen_umbralizada = cv2.threshold(imagen_grises, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif metodo_umbralizar == Umbralizacion.MetodoUmbralizado.fixed:
            ret, imagen_umbralizada = cv2.threshold(imagen_grises, umbral, 255, cv2.THRESH_BINARY)
        elif metodo_umbralizar == Umbralizacion.MetodoUmbralizado.adaptive:
            imagen_umbralizada = cv2.adaptiveThreshold(imagen_grises, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        return imagen_umbralizada
