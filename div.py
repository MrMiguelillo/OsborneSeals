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
file = sys.argv[1]
# Importar transcripción
transcripcion = sys.argv[2]
pag_izq = int(sys.argv[3])

# Parámetros modificables
erosion = 5
areaMinimaDePalabra = 2000
anchoMinimoDePalabra = 70
alturaMinimaDePalabra = 40

nombre = os.path.splitext(os.path.basename(file))[0]
path = os.path.dirname(file)
original = cv2.imread(file)

# Umbralizado de JSM
#img = umbralizaciones.umbralizar_imagen(file)
# Umbralizado nuestro
gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img = separar.borde(img)
# Calcular tamaño de imagen
fil_px, col_px = img.shape
# Plantilla de pertenencia
img_plant = img < 255

# Generar transcripción
texto = []
txt_pag = []
txt_documento = []
with open(transcripcion, 'r', encoding='utf8') as inputfile:
    for line in inputfile:
        texto.append(line.strip())
for z in range (1, len(texto)):
    #if texto[z] == "..........":
    if texto[z].count('.') > 7:
        txt_documento.append(txt_pag)
        txt_pag = []
    else:
        txt_pag.append([texto[z], texto[z].count(' ') + 1])
txt_documento.append(txt_pag)

# Separar columnas
if len(sys.argv) == 5:
    pag_der = int(sys.argv[4])
    num_paginas = 2
    hist_hor = separar.hor_hist(img_plant)

    for minTest in range(0, np.max(hist_hor)):
        div = separar.columnas(hist_hor, minTest)

        if np.isnan(div) == False:
            minCol = minTest
            print("Columnas: minTest = %d" % minCol)
            break

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
minimo = np.zeros(num_paginas)
for x in range(0, num_paginas):
    # Histograma vertical
    hist_ver = separar.vert_hist(img_plant[0:fil_px, tab[x]:tab[x+1]])
    # Filtrado
    hist_ver_filtrado.append(filtro.mediana(hist_ver, 10))

    for minTest in range(np.max(hist_ver_filtrado[x]) -1, 0, -1):

        # Separar filas
        ini_filas, fin_filas = separar.filas(hist_ver_filtrado[x], minTest)

        if len(ini_filas) == filas_txt[x]:
            minimo[x] = minTest
            print("Página %d: minTest = %d" % (x+1, minimo[x]))
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

        #print("%s - Página %d de %d - Fila %2d de %d - %s" % (nombre, x+1, num_paginas, y+1, num_filas[x], txt[x][y]))

        # Seleccionar fila
        fila_ero_bw = img_ero_bw[filas[x][0][y]:filas[x][1][y], filas[x][2]:filas[x][3]]
        # Componentes conexas
        label_image = measure.label(fila_ero_bw)

        num_palabras_fila = 0
        palabras_fila = []

        for region in measure.regionprops(label_image):

            minr, minc, maxr, maxc = region.bbox
            bbox_width = maxc - minc
            bbox_height = maxr - minr

            # skip small images
            if (region.area < areaMinimaDePalabra) \
                    | (bbox_width < anchoMinimoDePalabra) \
                    | (bbox_height < alturaMinimaDePalabra) \
                    | (bbox_width > (tab[x + 1] - tab[x]) * 0.9):
                continue

            num_palabras_fila += 1
            palabras_fila.append([minc + filas[x][2], minr + filas[x][0][y], maxc + filas[x][2], maxr + filas[x][0][y]])

        # Añadir número de palabras de una fila
        num_palabras_pagina.append(num_palabras_fila)
        # Ordenar palabras de una fila
        palabras_fila = sorted(palabras_fila, key=lambda coord: coord[0])
        # Añadir palabras de una fila
        palabras_pagina.append(palabras_fila)

    # Añadir número de palabras de una página
    num_palabras.append(num_palabras_pagina)
    # Añadir palabras de una página
    palabras.append(palabras_pagina)

print("Generando imágenes")
l = 1
p = 1
for x in range(0, num_paginas):
    for y in range(0, num_filas[x]):
        #print("Página %d de %d - Fila %2d de %2d:   %2d palabras" % (x + 1, num_paginas, y + 1, num_filas[x], num_palabras[x][y]))
        # Dibujar líneas de separación de filas
        cv2.line(original, (filas[x][2], filas[x][0][y]), (filas[x][3], filas[x][0][y]), (255, 0, 0), 5)
        cv2.line(original, (filas[x][2], filas[x][1][y]), (filas[x][3], filas[x][1][y]), (255, 0, 0), 5)
        # Dibujar número de línea
        cv2.putText(original, str(l), (filas[x][2], filas[x][1][y]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        l += 1
        # Imprimir texto
        #d.text((palabras[x][y][0][0] + 20, palabras[x][y][0][1] + 50), txt[x][y], font=font, fill=(0, 0, 255, 255))

        for z in range(0, num_palabras[x][y]):
            # Dibujar rectángulos de palabras
            cv2.rectangle(original, (palabras[x][y][z][0], palabras[x][y][z][1]), (palabras[x][y][z][2], palabras[x][y][z][3]), 0, 1)
            # Dibujar número de palabra
            cv2.putText(original, str(p), (palabras[x][y][z][0], palabras[x][y][z][1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            p += 1

filestring = '../../Osborne/%s_CC.png' % nombre
cv2.imwrite(filestring, original)





# Generar XML
filestring_xml = '%s/%s_xml.html' % (path, nombre)
xml = open(filestring_xml, 'w', encoding='utf8')

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
        position: absolute; left: 0em; top: -1em; z-index: 99; opacity: 1;
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
    .classic {background: #FFFFFF; border: 1px solid #7F7F7F; }
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

        if palabras[x][y] == []:
            palabras[x][y] = [[filas[x][2], filas[x][0][y], filas[x][3], filas[x][1][y]]]
            num_palabras[x][y] = 1

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
                  '<span> </div>\n' % (width, height, top, left, txt[x][y][0]))

xml.write('</body>\n</html>\n')
xml.close()








import matplotlib.pyplot as plt
fig = plt.figure(1)
if num_paginas == 2:
    ax = fig.add_subplot(311)
    ax.set_title('Histograma horizontal: %d páginas' % num_paginas)
    plt.plot(hist_hor)
    plt.plot([int(div), int(div)],[0, np.max(hist_hor)], 'r')
    plt.plot(minCol * np.ones(col_px), 'r')
    plt.axis([0, col_px, 0, np.max(hist_hor)])

    ax = fig.add_subplot(312)
    ax.set_title('Página derecha - Histograma vertical: %d filas' % num_filas[1])
    plt.plot(hist_ver_filtrado[1])
    plt.plot(minimo[1] * np.ones(fil_px), 'r')
    plt.plot(filas[1][0], minimo[1] * np.ones(num_filas[1]), 'ro')
    plt.plot(filas[1][1], minimo[1] * np.ones(num_filas[1]), 'bo')
    plt.axis([0, fil_px, 0, np.max(hist_ver_filtrado[1])])

    ax = fig.add_subplot(313)
    ax.set_title('Página izquierda - Histograma vertical: %d filas' % num_filas[0])
    plt.plot(hist_ver_filtrado[0])
    plt.plot(minimo[0] * np.ones(fil_px), 'r')
    plt.plot(filas[0][0], minimo[0] * np.ones(num_filas[0]), 'ro')
    plt.plot(filas[0][1], minimo[0] * np.ones(num_filas[0]), 'bo')
    plt.axis([0, fil_px, 0, np.max(hist_ver_filtrado[0])])

else:
    ax = fig.add_subplot(111)
    ax.set_title('Página 1 - Histograma vertical: %d filas' % num_filas[0])
    plt.plot(hist_ver_filtrado[0])
    plt.plot(minimo[0] * np.ones(fil_px), 'r')
    plt.plot(filas[0][0], minimo[0] * np.ones(num_filas[0]), 'ro')
    plt.plot(filas[0][1], minimo[0] * np.ones(num_filas[0]), 'bo')
    plt.axis([0, fil_px, 0, np.max(hist_ver_filtrado[0])])

plt.subplots_adjust(.03, .03, .97, .97)
plt.show()

