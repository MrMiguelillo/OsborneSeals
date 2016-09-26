import cv2
import numpy as np
from FuncionSellosCompleta import detectar_sello

img = cv2.imread('imgs/10_IMG_0003.png', 0)
img2, coords, nombre = detectar_sello(img)

print(coords)
