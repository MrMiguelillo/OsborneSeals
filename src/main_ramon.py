import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from scipy import signal

separar = Separacion.Separacion()

img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)
filas, colum = img.shape

print("Histograma horizontal")
hist_hor = separar.hor_hist(img)
#plt.figure(1)
#plt.plot(hist)
#plt.show()

print("Separar columnas")
div = separar.columnas(hist_hor)
#print(div)

#cv2.line(img, (div, 0), (div, 10000), 100, 5)
#cv2.line(img, (div,0), (div, filas), 100, 5)
#cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
#cv2.imshow('result', img)

print("Histograma vertical")
sub_img = img[0:filas,0:div]
hist_ver = separar.vert_hist(sub_img)

print("Filtrado")
filtrado = separar.filtro_mediana(hist_ver, 10)
filtrado = np.array(filtrado)

ini=[]
fin=[]
for x in range(0, filas-1):

    if (filtrado[x] == 0.) & (filtrado[x+1] !=0.):
        ini.append(x+1)

    if (filtrado[x] != 0.) & (filtrado[x+1] == 0.):
        fin.append(x)

print(ini)
print(fin)
tam=len(ini)
tam2=len(fin)
print(tam)
print(tam2)

res=[]
res.append(ini[0]/2)
for x in range(0, tam-1):

    res.append((fin[x]-ini[x+1])/2+ini[x+1])



print(res)





print("Resultados gráficos")
plt.figure(1)
plt.subplot(211)
plt.plot(hist_ver)
plt.subplot(212)
plt.plot(filtrado)
plt.plot(res,np.zeros(tam),'ro')
plt.show()

#cv2.waitKey()
#cv2.destroyAllWindows()