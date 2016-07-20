import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
from skimage import measure
from src import Separacion
from src import Filtros

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

print("Encontrar palabras")
kernel = np.ones((5,5),np.uint8)
img_ero = cv2.erode(img, kernel, iterations=3)
img_ero_bw = (img_ero<1).astype('uint8')


print("Resultados gráficos")
fig, ax = plt.subplots(1,1)
ax.imshow(orig)
#plt.set_cmap("gray")
plt.subplots_adjust(.01,.01,.99,.99)


for y in range(0, num_filas):

    fila_ero_bw = img_ero_bw[ini_filas[y]:fin_filas[y], 0:col_px]
    label_image = measure.label(fila_ero_bw)

    for region in measure.regionprops(label_image):

        # skip small images
        if region.area < 1000:
            continue

        # draw rectangle around segmented coins
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr + ini_filas[y]), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)

        ax.add_patch(rect)

plt.show()
