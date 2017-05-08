import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('C:/Users/Mike/Documents/memoria_tfg/Figuras/img_hist_otsu_contrast.png', cv2.IMREAD_GRAYSCALE)
plt.hist(img.ravel(), 256, [0, 256])
plt.grid(b=True, which='major', axis='y', color='#BCBCBC')
plt.show()
