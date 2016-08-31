import cv2
from enum import Enum


class MetodoUmbralizado(Enum):
    otsu = 0
    fixed = 1
    adaptive = 2


class Umbralizacion:
    def umbralizar_imagen(self, imagen_grises, metodo_umbralizar, umbral=180):
        imagen_umbralizada = imagen_grises

        if metodo_umbralizar == MetodoUmbralizado.otsu:
            ret, imagen_umbralizada = cv2.threshold(imagen_grises, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif metodo_umbralizar == MetodoUmbralizado.fixed:
            ret, imagen_umbralizada = cv2.threshold(imagen_grises, umbral, 255, cv2.THRESH_BINARY)
        elif metodo_umbralizar == MetodoUmbralizado.adaptive:
            imagen_umbralizada = cv2.adaptiveThreshold(imagen_grises, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        return imagen_umbralizada