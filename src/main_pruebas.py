import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import measure
from src import Separacion
from src import Filtros


import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb






'''

separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
orig = Image.open('../imgs/Narciso2.png')
ppi = orig.info['dpi']
original = cv2.imread('../imgs/Narciso2.png')

# Importar imagen binarizada
img = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
fil_px, col_px = img.shape

# Calcular tamaño de imagen en centímetros
fil_cm = fil_px/(ppi[0]*0.39370)
col_cm = col_px/(ppi[0]*0.39370)

# Plantilla de pertenencia
img_plant = img < 255

print("Separar filas")
# Histograma vertical
hist_ver = separar.vert_hist(img_plant)
# Filtrado
hist_ver_filtrado = filtro.mediana(hist_ver, 10)
# Separar filas
ini_filas, fin_filas = separar.filas(hist_ver_filtrado, 100)
num_filas = len(ini_filas)

print("Separar palabras")
kernel = np.ones((5,5),np.uint8)
img_ero = cv2.erode(img, kernel, iterations=2)
img_ero_plant = img_ero < 255
num_palabras = []
res=[]
z=0
for y in range(0, num_filas):
    # Seleccionar fila
    fila = img_ero_plant[ini_filas[y]:fin_filas[y], 0:col_px]
    # Histograma horizontal
    hist_fila = separar.hor_hist(fila)
    # Separar palabras
    minimo_hueco = 1
    minimo_palabra = 40
    ini_palabras, fin_palabras = separar.palabras(hist_fila, minimo_hueco, minimo_palabra)
    num_palabras.append(len(ini_palabras))

    print("Fila %d de %d - Encontradas %d palabras " % (y + 1, num_filas, num_palabras[y]))

    for x in range(0, num_palabras[y]):

        res.append([ini_palabras[x], ini_filas[y], fin_palabras[x], fin_filas[y]])
        # Seleccionar palabra
        palabra = img_ero_plant[res[z][1]:res[z][3], res[z][0]:res[z][2]]
        # Histograma vertical
        hist_palabra = separar.vert_hist(palabra)
        # Filtrado
        # hist_palabra_filtrada = filtro.mediana(hist_palabra, 5)
        # Ajustar palabras
        ini, fin = separar.ajustar(hist_palabra)
        res[z][1] = res[z][1] + ini
        res[z][3] = res[z][3] - fin

        L = measure.label(palabra)
        print("   Palabra %d - Componentes conexas: %d" % (z, np.max(L)))

        z += 1

total_palabras = len(res)
for z in range(0, total_palabras):
        #cv2.line(img_ero, (res[z][0], res[z][1]), (res[z][2], res[z][1]), 100, 1)
        #cv2.line(img_ero, (res[z][2], res[z][1]), (res[z][2], res[z][3]), 100, 1)
        #cv2.line(img_ero, (res[z][2], res[z][3]), (res[z][0], res[z][3]), 100, 1)
        #cv2.line(img_ero, (res[z][0], res[z][3]), (res[z][0], res[z][1]), 100, 1)


im2 = cv2.findContours(img_ero,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im2)
print("Resultados gráficos")
#cv2.imwrite('../prueba_compconex.png', img)
plt.figure(1)
plt.subplots_adjust(.01,.01,.99,.99)
plt.set_cmap("gray")
plt.imshow(im2)
plt.show()
#plt.figure(2)
#plt.plot(filtrado)
#plt.show()
'''

#image = data.coins()[50:-50, 50:-50]
#image = cv2.imread('../imgs/Narciso2.png', 0)
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
ima = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
kernel = np.ones((5,5),np.uint8)
img = cv2.erode(ima, kernel, iterations=2)
image = (img<1).astype('uint8')




#bw = cleared

# apply threshold
#thresh = threshold_otsu(image)
#bw = closing(image > thresh, square(3))

# remove artifacts connected to image border
#cleared = bw.copy()
#clear_border(cleared)

# label image regions
label_image = label(image)

#borders = np.logical_xor(bw, cleared)
#label_image[borders] = -1
#image_label_overlay = label2rgb(label_image, image=image)




#fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
fig, ax = plt.subplots(1,1)
plt.set_cmap("gray")
#ax.imshow(image_label_overlay)
ax.imshow(img)

for region in regionprops(label_image):

    # skip small images
    if region.area < 300:
        continue

    # draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)

    ax.add_patch(rect)


#plt.set_cmap("gray")
plt.show()