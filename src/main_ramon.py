import cv2
import numpy as np
import matplotlib.pyplot as plt
from src import Separacion
from scipy import signal
#from oct2py import octave

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
sub_img = img[0:div, 0:filas]
hist_ver = separar.vert_hist(sub_img)


prueba = signal.find_peaks_cwt(hist_ver,np.arange(1,14))
#(peaks, indexes) = octave.findpeaks(hist_ver, 'DoubleSided','MinPeakHeight', 0.04,'MinPeakDistance', 100,'MinPeakWidth', 0)
print(prueba)
tam=len(prueba)
print(tam)

print("Resultados gráficos")
plt.figure(1)
#plt.subplot(211)
plt.plot(hist_ver)
#plt.subplot(212)
plt.plot(prueba,hist_ver[prueba],'ro')
plt.show()

#cv2.waitKey()
#cv2.destroyAllWindows()