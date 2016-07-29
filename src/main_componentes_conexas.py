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
#orig = Image.open('../imgs/Narciso2.png')
orig = Image.open('../imgs/IMG_0003.png')
ppi = orig.info['dpi']
#original = cv2.imread('../imgs/Narciso2.png')
original = cv2.imread('../imgs/IMG_0003.png')

# Importar imagen binarizada
#img = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
img = cv2.imread('../IMG_0003_met_0_vec_3_sig_-1_thr_0.png', 0)
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
z = 0

for y in range(0, num_filas):

    # Dibujar líneas de separación de filas
    #cv2.line(original, (0, ini_filas[y]), (col_px, ini_filas[y]), 0, 1)
    #cv2.line(original, (0, fin_filas[y]), (col_px, fin_filas[y]), 0, 1)

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

        z = z + 1

        #print("T_1892.01.25 \t %2d \t %7d \t %7d \t %7d \t %7d" % (z, minc, minr + ini_filas[y], maxc, maxr + ini_filas[y]))

        rect = mpatches.Rectangle((minc, minr + ini_filas[y]), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

        cv2.rectangle(original, (minc, minr + ini_filas[y]), (maxc, maxr + ini_filas[y]), 0, 1)

        texto = str(z)
        cv2.putText(original, texto, (minc, maxr + ini_filas[y] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)

    #print("Fila %d de %d:   %d palabras" % (y, num_filas - 1, palabras[y]))

'''
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


'''
groundtruth = []

with open('../T_1892.01.25_erosion_3.txt') as inputfile:
    for line in inputfile:
        groundtruth.append(line.strip().split('\t'))

tam_groundtruth = len(groundtruth)

SI = np.zeros(tam_groundtruth)
SA = np.zeros(tam_groundtruth)
SB = np.zeros(tam_groundtruth)
ST = np.zeros(tam_groundtruth)
ratio = np.zeros(tam_groundtruth)
aciertos = 0

for x in range(0, tam_groundtruth):
    for z in range(0, len(res)):

        XA1 = res[z][0]
        YA1 = res[z][1]
        XA2 = res[z][2]
        YA2 = res[z][3]
        XG1 = int(groundtruth[x][3])
        YG1 = int(groundtruth[x][4])
        XG2 = int(groundtruth[x][5])
        YG2 = int(groundtruth[x][6])

        SI = np.max([0, (np.min([XA2, XG2]) - np.max([XA1, XG1]))]) * np.max([0, (np.min([YA2, YG2]) - np.max([YA1, YG1]))])

        if SI > 0:

            SA = (XA2 - XA1) * (YA2 - YA1)
            SB = (XG2 - XG1) * (YG2 - YG1)

            ratio[x] = np.max([ratio[x], SI/(SA+SB-SI)])

    if ratio[x] > 0.8:

        aciertos = aciertos + 1

print("149: %d aciertos de %d. %f %% por ciento de efectividad" % (aciertos, tam_groundtruth, aciertos/tam_groundtruth*100))



cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', original)
#cv2.imwrite('../comp_conx.png', original)



plt.show()