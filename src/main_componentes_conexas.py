import cv2
import numpy as np
import os
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

# Parámetros modificables
num_paginas = 2
pag_izq = 2
pag_der = 3

# Importar transcripción
#transcripcion = '../T_1892.01.25.txt'
transcripcion = '../1882-L123.M17.T_2.txt'

# Importar imagen original
#file = '../imgs/Narciso2.png'
file = '../imgs/IMG_0003.png'

# Importar imagen binarizada
# Umbralizado de JSM
#img = umbralizar.umbralizar_imagen(file)
# Umbralizado nuestro
#img = cv2.imread('../Narciso2_met_1_vec_0_sig_0_thr_134.png', 0)
img = cv2.imread('../0003_sin_escudo_met_0_vec_0_sig_0_thr_0.png', 0)

nombre = os.path.splitext(os.path.basename(file))[0]
orig = Image.open(file)
original = cv2.imread(file)
font = ImageFont.truetype("Arial.ttf",40)
d = ImageDraw.Draw(orig)

# Calcular tamaño de imagen en centímetros
ppi = orig.info['dpi']
fil_px, col_px = img.shape
fil_cm = fil_px/(ppi[0]*0.39370)
col_cm = col_px/(ppi[0]*0.39370)

# Plantilla de pertenencia
img_plant = img < 255

print('Generar transcripción')
texto = []
txt_pag = []
txt_documento = []
with open(transcripcion) as inputfile:
    for line in inputfile:
        #texto.append(line.strip().split('\t'))
        texto.append(line.strip())

for z in range (1, len(texto)):
    if texto[z] == "..........":
        txt_documento.append(txt_pag)
        txt_pag = []
    else:
        txt_pag.append(texto[z])
txt_documento.append(txt_pag)

print("Separar columnas")
if num_paginas == 2:
    hist_hor = separar.hor_hist(img_plant)
    div = separar.columnas(hist_hor)
    tab = [0, div, col_px]
    txt = [txt_documento[pag_izq - 1], txt_documento[pag_der - 1]]
else:
    tab = [0, col_px]
    txt = [txt_documento[pag_izq - 1]]

print("Separar filas")
filas = []
num_filas = []
for x in range(0, num_paginas):
    # Histograma vertical
    hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x+1]])
    # Filtrado
    hist_ver_filtrado = filtro.mediana(hist_ver, 10)
    # Separar filas
    ini_filas, fin_filas = separar.filas(hist_ver_filtrado, 100)
    # Toma de datos
    num_filas.append(len(ini_filas))
    filas.append([ini_filas, fin_filas, tab[x], tab[x + 1]])

print("Encontrar palabras")
kernel = np.ones((5, 5), np.uint8)
img_ero = cv2.erode(img, kernel, iterations=5)
img_ero_bw = (img_ero < 1).astype('uint8')

#print("Resultados gráficos")
#fig, ax = plt.subplots(1, 1)
#ax.imshow(orig)
##plt.set_cmap("gray")
#plt.subplots_adjust(.01, .01, .99, .99)

num_palabras = []
palabras = []
for x in range(0, num_paginas):
    num_palabras_pagina = []
    palabras_pagina = []
    for y in range(0, num_filas[x]):
        # Seleccionar fila
        fila_ero_bw = img_ero_bw[filas[x][0][y]:filas[x][1][y], filas[x][2]:filas[x][3]]
        # Componentes conexas
        label_image = measure.label(fila_ero_bw)

        num_palabras_fila = 0
        palabras_fila = []

        for region in measure.regionprops(label_image):
            # skip small images
            if region.area < 1000:
                continue

            num_palabras_fila += 1
            minr, minc, maxr, maxc = region.bbox
            palabras_fila.append([minc + filas[x][2], minr + filas[x][0][y], maxc + filas[x][2], maxr + filas[x][0][y]])

            #rect = mpatches.Rectangle((minc, minr + ini_filas[y]), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=1)
            #ax.add_patch(rect)

        # Añadir número de palabras de una fila
        num_palabras_pagina.append(num_palabras_fila)

        # Ordenar palabras de una fila
        palabras_fila = sorted(palabras_fila, key=lambda coord: coord[0])
        # Añadir palabras de una fila
        palabras_pagina.append(palabras_fila)

    num_palabras.append(num_palabras_pagina)
    palabras.append(palabras_pagina)

l = 1
p = 1
for x in range(0, num_paginas):
    for y in range(0, num_filas[x]):
        print("Página %d de %d - Fila %d de %d:   %d palabras" % (x + 1, num_paginas, y + 1, num_filas[x], num_palabras[x][y]))
        # Dibujar líneas de separación de filas
        #cv2.line(original, (filas[x][2], filas[x][0][y]), (filas[x][3], filas[x][0][y]), 0, 1)
        #cv2.line(original, (filas[x][2], filas[x][1][y]), (filas[x][3], filas[x][1][y]), 0, 1)
        # Dibujar número de línea
        #cv2.putText(original, str(l), (palabras[x][y][0][0], filas[x][1][y]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        l += 1
        # Imprimir texto
        d.text((palabras[x][y][0][0] + 20, palabras[x][y][0][1] + 50), txt[x][y], font=font, fill=(0, 0, 255, 255))

        for z in range(0, num_palabras[x][y]):
            # Imprimir coordenadas de cada palabra
            #print("T_1892.01.25 \t %4d \t %7d \t %7d \t %7d \t %7d" % (p, pagina[y][z][0], pagina[y][z][1], pagina[y][z][2], pagina[y][z][3]))
            # Dibujar rectángulos de palabras
            #cv2.rectangle(original, (palabras[x][y][z][0], palabras[x][y][z][1]), (palabras[x][y][z][2], palabras[x][y][z][3]), 0, 1)
            # Dibujar número de palabra
            #cv2.putText(original, str(p), (palabras[x][y][z][0], palabras[x][y][z][1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            p += 1

# Generar XML
filestring = '../../../Osborne/RepoOsborne/ResultadosOCR/%s_xml.txt' % (nombre)
xml = open(filestring, 'w')

cabecera = """"<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>ToolTips Example</title>
    <style type="text/css">
    .tooltip {
        border-bottom: 1px dotted #000000; color: #000000; outline: none;
        cursor: help; text-decoration: none;
        position: relative;
    }
    .tooltip span {
        margin-left: -999em;
        position: absolute;
    }
    .tooltip:hover span {
        border-radius: 1px 1px; -moz-border-radius: 1px; -webkit-border-radius: 1px;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.1); -webkit-box-shadow: 5px 5px rgba(0, 0, 0, 0.1); -moz-box-shadow: 5px 5px rgba(0, 0, 0, 0.1);
        font-family: Calibri, Tahoma, Geneva, sans-serif; font-size: 1vw; color:blue; text-align: center;
        position: absolute; left: 0em; top: 0em; z-index: 99; opacity: 0.5;
        margin-left: 0; width: 90%;
    }
    .tooltip:hover img {
        border: 0; margin: -10px 0 0 -55px;
        float: left; position: absolute;
    }
    .tooltip:hover em {
        font-family: Candara, Tahoma, Geneva, sans-serif; font-size: 1.2em; font-weight: bold;
        display: block; padding: 0.2em 0 0.6em 0;
    }
    .classic { padding: 0.8em 1em; }
    .custom { padding: 0.5em 0.8em 0.8em 2em; }
    * html a:hover { background: transparent; }
    .classic {background: #FFFFAA; border: 1px solid #FFAD33; }
    .critical { background: #FFCCAA; border: 1px solid #FF3334;	}
    .help { background: #9FDAEE; border: 1px solid #2BB0D7;	}
    .info { background: #9FDAEE; border: 1px solid #2BB0D7;	}
    .warning { background: #FFFFAA; border: 1px solid #FFAD33; }
    </style>
</head>
 <body>
 """

xml.write(cabecera)
xml.write('<img src="%s.png" alt="Documento Osborne" style="position: absolute; width:90%%"></img>\n' % (nombre))

for x in range(0, num_paginas):
    for y in range(0, num_filas[x]):

        B1 = -1
        for z in range(0, num_palabras[x][y]):

            if palabras[x][y][z][2] > B1:
                B1 = palabras[x][y][z][2]

        cv2.rectangle(original, (palabras[x][y][0][0], filas[x][0][y]), (B1, filas[x][1][y]), 0, 1)
        #cv2.rectangle(original, (palabras[x][y][0][0], filas[x][0][y]), (palabras[x][y][len(palabras[x][y])-1][2], filas[x][1][y]), 0, 1)

        left = (palabras[x][y][0][0]/col_px)*0.9*100
        top = (filas[x][0][y] / col_px) * 0.9 * 100

        width = ((B1 - palabras[x][y][0][0])/col_px)*0.9*100
        height = ((filas[x][1][y] - filas[x][0][y])/col_px)*0.9*100

        xml.write('<div class="tooltip" style="position: absolute;  width:%.2fvw; height:%.2fvw; top:%.2fvw;'
                  'left: %.2fvw; border:0px solid #0000FF;"> <span class = "classic"> %s'
                  '<span> </div>\n' % (width, height, top, left, txt[x][y]))

xml.write('</body>\n'
          '</html>\n')
xml.close()
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
filestring = '../../../Osborne/RepoOsborne/ResultadosOCR/%s_comp_conx_pruebas.png' % (nombre)
cv2.imwrite(filestring, original)
filestring = '../../../Osborne/RepoOsborne/ResultadosOCR/%s_comp_conx_texto_pruebas.png' % (nombre)
#orig.save(filestring)
#plt.show()
