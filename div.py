import cv2
import numpy as np
import os
import sys
from skimage import measure
import Separacion
import Filtros
import Umbralizaciones

umbralizaciones = Umbralizaciones.Umbralizaciones()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()

# Importar imagen original
#file = 'imgs/0003_sin_escudo.png'
#file = 'imgs/Narciso2.png'
#file = '../../Osborne/RepoOsborne/documentos/1883-L119.M29/2/IMG_0001.png'
file = sys.argv[1]
# Importar transcripción
#transcripcion = 'tran/1882-L123.M17.T_2.txt'
#transcripcion = 'tran/T_2_2.txt'
#transcripcion = 'tran/T_1892.01.25.txt'
transcripcion = sys.argv[2]
#pag_izq = 1
pag_izq = int(sys.argv[3])

# Parámetros modificables
erosion = 5

nombre = os.path.splitext(os.path.basename(file))[0]
path = os.path.dirname(file)
original = cv2.imread(file)

# Umbralizado de JSM
#img = umbralizaciones.umbralizar_imagen(file)
# Umbralizado nuestro
gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Calcular tamaño de imagen
fil_px, col_px = img.shape
# Plantilla de pertenencia
img_plant = img < 255

# Generar transcripción
texto = []
txt_pag = []
txt_documento = []
with open(transcripcion) as inputfile:
    for line in inputfile:
        texto.append(line.strip())
for z in range (1, len(texto)):
    if texto[z] == "..........":
        txt_documento.append(txt_pag)
        txt_pag = []
    else:
        txt_pag.append(texto[z])
txt_documento.append(txt_pag)

# Separar columnas
if len(sys.argv) == 5:
    pag_der = int(sys.argv[4])
    num_paginas = 2
    hist_hor = separar.hor_hist(img_plant)
    div = separar.columnas(hist_hor)
    tab = [0, int(div), col_px]
    txt = [txt_documento[pag_izq - 1], txt_documento[pag_der - 1]]
    filas_txt = [len(txt[0]), len(txt[1])]
else:
    num_paginas = 1
    tab = [0, col_px]
    txt = [txt_documento[pag_izq - 1]]
    filas_txt = [len(txt[0])]

# Separar filas
filas = []
num_filas = []
hist_ver_filtrado = []
for x in range(0, num_paginas):
    # Histograma vertical
    hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x+1]])
    # Filtrado
    hist_ver_filtrado.append(filtro.mediana(hist_ver, 10))

    for minTest in range(0, np.max(hist_ver_filtrado[x]) -1, 1):

        # Separar filas
        ini_filas, fin_filas = separar.filas(hist_ver_filtrado[x], minTest)

        if len(ini_filas) == filas_txt[x]:
            # Toma de datos
            num_filas.append(len(ini_filas))
            filas.append([ini_filas, fin_filas, tab[x], tab[x + 1]])
            break

# Encontrar palabras
kernel = np.ones((5, 5), np.uint8)
img_ero = cv2.erode(img, kernel, iterations=erosion)
img_ero_bw = (img_ero < 1).astype('uint8')

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

        # Añadir número de palabras de una fila
        num_palabras_pagina.append(num_palabras_fila)
        # Ordenar palabras de una fila
        palabras_fila = sorted(palabras_fila, key=lambda coord: coord[0])
        # Añadir palabras de una fila
        palabras_pagina.append(palabras_fila)

    num_palabras.append(num_palabras_pagina)
    palabras.append(palabras_pagina)

# Generar XML
filestring_xml = '%s/%s_xml.html' % (path, nombre)
xml = open(filestring_xml, 'w')

cabecera = """<!DOCTYPE html>
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
        font-family: Calibri, Tahoma, Geneva, sans-serif; font-size: 2vw; color:blue; text-align: center;
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
    .classic { padding: 0.1em 1em; }
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

        left = (palabras[x][y][0][0] / col_px) * 0.9 * 100
        top = (filas[x][0][y] / col_px) * 0.9 * 100

        width = ((B1 - palabras[x][y][0][0]) / col_px) * 0.9 * 100
        height = ((filas[x][1][y] - filas[x][0][y]) / col_px) * 0.9 * 100

        xml.write('<div class="tooltip" style="position: absolute;  width:%.2fvw; height:%.2fvw; top:%.2fvw;'
                  'left: %.2fvw; border:0px solid #0000FF;"> <span class = "classic"> %s'
                  '<span> </div>\n' % (width, height, top, left, txt[x][y]))

xml.write('</body>\n</html>\n')
xml.close()