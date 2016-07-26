import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy
from PIL import Image
from skimage import measure
from scipy import ndimage
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
img_ero = cv2.erode(img, kernel, iterations = 3)
img_ero_bw = (img_ero < 1).astype('uint8')

print("Resultados gráficos")
fig, ax = plt.subplots(1,1)
ax.imshow(orig)
#plt.set_cmap("gray")
plt.subplots_adjust(.01,.01,.99,.99)

res = []
palabras = np.zeros(num_filas)

for y in range(0, num_filas):

    # Dibujar líneas de separación de filas
    cv2.line(original, (0, ini_filas[y]), (col_px, ini_filas[y]), 0, 1)
    cv2.line(original, (0, fin_filas[y]), (col_px, fin_filas[y]), 0, 1)

    # Seleccionar fila
    fila_ero_bw = img_ero_bw[ini_filas[y]:fin_filas[y], 0:col_px]
    # Componentes conexas
    label_image = measure.label(fila_ero_bw)

    palabras[y] = 0

    for region in measure.regionprops(label_image):

        # skip small images
        if region.area < 1000:
            continue

        palabras[y] = palabras[y] + 1

        minr, minc, maxr, maxc = region.bbox

        res.append([minc, minr + ini_filas[y], maxc, maxr + ini_filas[y]])

        rect = mpatches.Rectangle((minc, minr + ini_filas[y]), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

        cv2.line(original, (minc, minr + ini_filas[y]), (maxc, minr + ini_filas[y]), 0, 1)
        cv2.line(original, (minc, minr + ini_filas[y]), (minc, maxr + ini_filas[y]), 0, 1)
        cv2.line(original, (minc, maxr + ini_filas[y]), (maxc, maxr + ini_filas[y]), 0, 1)
        cv2.line(original, (maxc, minr + ini_filas[y]), (maxc, maxr + ini_filas[y]), 0, 1)

    print("Fila %d de %d:   %d palabras" % (y, num_filas - 1, palabras[y]))

integ = cv2.integral(palabras)

# Línea inferior
for y in range(0, num_filas - 1):
    # Final de la actual e inicial de la siguiente
    if fin_filas[y] == ini_filas[y + 1]:
        # Para cada palabra de la fila
        for x in range(int(integ[y][1]), int(integ[y + 1][1]) - 1):
            # Si coincide con la final
            if res[x][3] == fin_filas[y]:

                cv2.line(original, (res[x][0], res[x][3]), (res[x][2], res[x][3]), 255, 1)

# Línea superior
for y in range(1, num_filas):
    # Final de la anterior e inicial de la actual
    if fin_filas[y - 1] == ini_filas[y]:
        # Para cada palabra de la fila
        for x in range(int(integ[y][1]), int(integ[y + 1][1]) - 1):
            # Si coincide con la inicial
            if res[x][1] == ini_filas[y]:

                cv2.line(original, (res[x][0], res[x][1]), (res[x][2], res[x][1]), 255, 1)

cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', original)
cv2.imwrite('../comp_conx.png', original)

plt.show()