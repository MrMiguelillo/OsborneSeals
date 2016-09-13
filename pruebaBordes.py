import cv2
import os
import Separacion

separar = Separacion.Separacion()

file = 'imgs/Narciso2.png'
nombre = os.path.splitext(os.path.basename(file))[0]
path = os.path.dirname(file)
original = cv2.imread(file)

gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

imgSinBorde = separar.borde(img)

filestring = '../../Osborne/%s_SinBorde.png' % (nombre)
cv2.imwrite(filestring, imgSinBorde)

