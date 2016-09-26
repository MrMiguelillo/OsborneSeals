# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import sys
from skimage import measure
import Separacion
import Filtros
import Umbralizaciones
import codecs
import random
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

umbralizaciones = Umbralizaciones.Umbralizaciones()
separar = Separacion.Separacion()
filtro = Filtros.Filtros()
# Importar imagen original
file = sys.argv[1]
print(file)
pag_izq = int(sys.argv[3])

# Parametros modificables
erosion = 5
areaMinimaDePalabra = 2000
anchoMinimoDePalabra = 70
alturaMinimaDePalabra = 40

nombre = os.path.splitext(os.path.basename(file))[0]
path = os.path.dirname(file)
original = cv2.imread(file)

# Umbralizado de JSM
# img = umbralizaciones.umbralizar_imagen(file)
# Umbralizado nuestro
gray_img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img = separar.borde(img)
# Calcular tamano de imagen
fil_px, col_px = img.shape
# Plantilla de pertenencia
img_plant = img < 255

# Generar transcripcion
txt_pag = []
txt_documento = []

# Generar transcripcion: Cuando se mete un .txt

#Get the transcription as a string	
transcripcion = sys.argv[2]
texto =[]
with open(transcripcion, 'r', encoding='utf8') as inputfile:
    for line in inputfile:
        texto.append(line.strip())

# Generar transcripcion: Cuadno se mete un string
#texto = [int(e) if e.isdigit() else e for e in transcripcion.split('\n')]
# texto = unicode(texto_ascii, "")

# print("\nHe recibido la transcripcion: %s" % transcripcion)
# texto = transcripcion
# trozos = texto.split('\\n')
# numeroRandom = random.randint(1, 999999)

#CREATE A FILE WITH A RANDOM NAME
# print(numeroRandom)

# f = open("transcripcion"+str(numeroRandom)+".txt", "w")
# for i in range (0 , len(trozos)):
    # f.write(trozos[i]+"\n")
# f.close()

# texto = []
#OPEN THE FILE
# with open("transcripcion"+str(numeroRandom)+".txt", 'r', encoding='utf8') as inputfile:
    # for line in inputfile:
        # texto.append(line.strip())

for z in range (1, len(texto)):
    # if texto[z] == "..........":
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
    
    for minTest in range(np.max(hist_ver_filtrado[x]) - 1, 0, -1):
        # Separar filas
        ini_filas, fin_filas = separar.filas(hist_ver_filtrado[x], minTest)
        if len(ini_filas) == filas_txt[x]:
            minimo[x] = minTest
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

        # Anadir numero de palabras de una fila
        num_palabras_pagina.append(num_palabras_fila)
        # Ordenar palabras de una fila
        palabras_fila = sorted(palabras_fila, key=lambda coord: coord[0])
        # Anadir palabras de una fila
        palabras_pagina.append(palabras_fila)

    # Anadir numero de palabras de una pagina
    num_palabras.append(num_palabras_pagina)
    # Anadir palabras de una pagina
    palabras.append(palabras_pagina)

# Generar XML
filestring_xml = '%s/%s_xml.html' % (path, nombre)
xml = open(filestring_xml, 'w', encoding='utf8')

cabecera = ""
xml.write(cabecera)

urlImage = path.split('archivoHistorico')
xml.write('<div style="overflow: hidden;" id="myImagePosition" class="modal-content">')
# xml.write('<img src="http://146.255.101.63%s/%s.png" alt="Documento Osborne" width="100%%"></img>\n' % (urlImage[1], nombre))
xml.write('<span class="closeModalWindow" >&times;</span>')
xml.write('<img id="imageWithDivs" src="" alt="Documento Osborne" width="100%%"></img>\n')

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

        xml.write('<div class="divTranscription" style="position: absolute;  width:%.2fvw; height:%.2fvw; top:%.2fvw;'
                  'left: %.2fvw; border:0px solid #0000FF;"> <span style="display:none" class = "classic"> %s'
                  '<span> </div>\n' % (width, height, top, left, txt[x][y][0]))
			  
xml.write('</div>')
#xml.write('</body>\n</html>\n')
xml.close()

##REMOVE THE TXT FILE OF THE TRANSCRIPTION
# os.remove("transcripcion"+str(numeroRandom)+".txt")