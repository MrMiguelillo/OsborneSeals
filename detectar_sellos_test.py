import cv2
import numpy as np
from FuncionSellosCompleta import detectar_sello

img = cv2.imread('C:/Users/usuario/Desktop/document/1884-L123.M18/145/IMG_0001.png', 0)
img2, coords, nombre = detectar_sello(img)

print(coords)
