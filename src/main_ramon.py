import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from src import Filtros

separar = Separacion.Separacion()
filtros = Filtros.Filtros()

img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)
filas, colum = img.shape

print("Histograma horizontal")
hist_hor = separar.hor_hist(img)
#plt.figure(1)
#plt.plot(hist)
#plt.show()

print("Separar columnas")
div = separar.columnas(hist_hor)

print("Histograma vertical")
#sub_img = img[0:filas,0:div]
sub_img = img[0:filas,div:colum]
hist_ver = separar.vert_hist(sub_img)

print("Filtrado")

filtrado = filtros.mediana(hist_ver, 10)
# filtrado = np.array(filtrado)

print("Separar filas")
inicios,finales = separar.filas(filtrado)
tam1 = len(inicios)
tam2 = len(finales)


cv2.line(img, (div,0), (div, filas), 100, 5)

for x in range(1,tam1):
    cv2.line(img, (div,inicios[x]), (colum,inicios[x]), 100, 5)

for x in range(1, tam2):
    cv2.line(img, (div,finales[x]), (colum,finales[x]), 100, 5)

cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', img)


print("Resultados gráficos")
plt.figure(1)
plt.subplot(211)
plt.plot(hist_ver)
plt.subplot(212)
plt.plot(filtrado)
plt.plot(inicios,np.ones(tam1)*100,'ro')
plt.plot(finales,np.ones(tam2)*200,'bo')
plt.show()



#cv2.waitKey()
#cv2.destroyAllWindows()