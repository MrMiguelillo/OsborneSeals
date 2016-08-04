import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy
from PIL import Image, ImageDraw, ImageFont
from skimage import measure
from scipy import ndimage
from src import Separacion
from src import Filtros
from src import Umbralizaciones


umbralizar = Umbralizaciones.Umbralizaciones()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
orig = Image.open('../imgs/IMG_001.png')

font = ImageFont.truetype("Arial.ttf",40)
d = ImageDraw.Draw(orig)
ppi = orig.info['dpi']


original = cv2.imread('../imgs/IMG_001.png')

# Importar imagen binarizada
img = umbralizar.umbralizar_imagen('../imgs/IMG_001.png')
fil_px, col_px = img.shape

# Calcular tamaño de imagen en centímetros
fil_cm = fil_px/(ppi[0]*0.39370)
col_cm = col_px/(ppi[0]*0.39370)

# Plantilla de pertenencia
img_plant = img < 255

print("Separar columnas")
hist_hor = separar.hor_hist(img_plant)
div = separar.columnas(hist_hor)

print("Separar filas")
# Histograma vertical
hist_ver1 = separar.vert_hist(img_plant[0:fil_px, 0:div])
hist_ver2 = separar.vert_hist(img_plant[0:fil_px, div:col_px])
# Filtrado
hist_ver_filtrado1 = filtro.mediana(hist_ver1, 10)
hist_ver_filtrado2 = filtro.mediana(hist_ver2, 10)

# Separar filas
ini_filas1, fin_filas1 = separar.filas(hist_ver_filtrado1, 100)
ini_filas2, fin_filas2 = separar.filas(hist_ver_filtrado2, 100)
num_filas = len(ini_filas1) + len(ini_filas2)

ini_filas = ini_filas1.copy()
ini_filas.extend(ini_filas2)
fin_filas = fin_filas1.copy()
fin_filas.extend(fin_filas2)

izq_filas = np.zeros(num_filas)
der_filas = np.zeros(num_filas)

izq_filas[0:len(ini_filas1)] = 0
der_filas[0:len(ini_filas1)] = div
izq_filas[len(ini_filas1):num_filas] = div
der_filas[len(ini_filas1):num_filas] = col_px
izq_filas = izq_filas.astype('int')
der_filas = der_filas.astype('int')

print(izq_filas)

print("Encontrar palabras")
kernel = np.ones((5, 5), np.uint8)
img_ero = cv2.erode(img, kernel, iterations=3)
img_ero_bw = (img_ero < 1).astype('uint8')

#print("Resultados gráficos")
#fig, ax = plt.subplots(1, 1)
#ax.imshow(orig)
##plt.set_cmap("gray")
#plt.subplots_adjust(.01, .01, .99, .99)

# Importar transcripción
texto = []
pag = []
documento = []
with open('../1882-L123.M17.T_2.txt') as inputfile:
    for line in inputfile:
        #texto.append(line.strip().split('\t'))
        texto.append(line.strip())

for z in range (1, len(texto)):
    if texto[z] == "..........":
        documento.append(pag)
        pag = []
    else:
        pag.append(texto[z])

txt = documento[1].copy()
txt.extend(documento[2])

#texto = []
#with open('../T_1892.01.25.txt') as inputfile:
#    for line in inputfile:
#        texto.append(line.strip())

res = []
palabras = np.zeros(num_filas)
pagina = []
z = 0

for y in range(0, num_filas):

    # Seleccionar fila
    fila_ero_bw = img_ero_bw[ini_filas[y]:fin_filas[y], izq_filas[y]:der_filas[y]]
    # Componentes conexas
    label_image = measure.label(fila_ero_bw)

    palabras[y] = 0
    linea = []

    for region in measure.regionprops(label_image):

        # skip small images
        if region.area < 1000:
            continue

        palabras[y] = palabras[y] + 1
        minr, minc, maxr, maxc = region.bbox
        linea.append([minc + izq_filas[y], minr + ini_filas[y], maxc + izq_filas[y], maxr + ini_filas[y]])

        #rect = mpatches.Rectangle((minc, minr + ini_filas[y]), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)
        #ax.add_patch(rect)

    # Ordenar palabras de una línea
    linea = sorted(linea, key=lambda coord: coord[0])
    # Añadir palabras de una línea
    pagina.append(linea)

print("Resultados gráficos")
p = 1
for y in range(0, len(pagina)):
    print("Fila %d de %d:   %d palabras" % (y, num_filas - 1, palabras[y]))
    # Dibujar líneas de separación de filas
    cv2.line(original, (izq_filas[y], ini_filas[y]), (der_filas[y], ini_filas[y]), 0, 1)
    cv2.line(original, (izq_filas[y], fin_filas[y]), (der_filas[y], fin_filas[y]), 0, 1)
    # Dibujar número de línea
    #cv2.putText(original, str(y), (pagina[y][0][0], fin_filas[y]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
    # Imprimir texto
    #d.text((pagina[y][0][0] + 20, pagina[y][0][1] + 50), txt[y], font=font, fill=(0, 0, 255, 255))
    for z in range(0, int(palabras[y])):
        # Imprimir coordenadas de cada palabra
        #print("T_1892.01.25 \t %4d \t %7d \t %7d \t %7d \t %7d" % (p, pagina[y][z][0], pagina[y][z][1], pagina[y][z][2], pagina[y][z][3]))
        # Dibujar rectángulos de palabras
        cv2.rectangle(original, (pagina[y][z][0], pagina[y][z][1]), (pagina[y][z][2], pagina[y][z][3]), 0, 1)
        # Dibujar número de palabra
        cv2.putText(original, str(p), (pagina[y][z][0], pagina[y][z][1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        p += 1

'''
# Detectar lados de palabras que se unen con otras líneas
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

'''
# Pruebas para comparar la efectividad del código
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
'''
print("Generando imágenes")
#cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
#cv2.imshow('result', original)
cv2.imwrite('../comp_conx.png', original)
cv2.imwrite('../img.png', img)

orig.save("../comp_conx_texto.png")
#plt.show()