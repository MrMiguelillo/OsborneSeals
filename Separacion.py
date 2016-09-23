import numpy as np
from skimage import measure

class Separacion:
    def vert_hist(self, img):
        hist = np.sum(img, 1)
        return hist

    def hor_hist(self, img):
        hist = np.sum(img, 0)
        return hist

    # Entrada: Histograma horizontal
    # Salida: Tuplet: (Coordenada horizontal de la división de la página, longitud de la racha máxima de mínimos en el
    #       histograma). El segundo valor del tuplet se utiliza para saber si el documento tiene una columna de texto
    #       únicamente y no necesita ser dividido
    def columnas(self, histograma, minimo):
        long = histograma.size
        min_i = round(long / 3, 0)
        max_i = round(2 * long / 3, 0)
        suma = 0
        hueco = 0
        tam_hueco = 0
        min_x_actual = float('Inf')
        max_x_actual = 0
        min_x_hueco = float('Inf')
        max_x_hueco = 0

        for x in range(int(min_i), int(max_i)):
            if histograma[x] <= minimo:
                suma += 1
                if min_x_actual == float('Inf'):
                    min_x_actual = x
            else:
                hueco = suma
                suma = 0
                max_x_actual = x

            if hueco > tam_hueco:
                tam_hueco = hueco
                min_x_hueco = min_x_actual
                max_x_hueco = max_x_actual

        res_x = round((max_x_hueco - min_x_hueco) / 2, 0) + min_x_hueco
        return res_x

    # Entrada: Histograma vertical
    # Entrada: Valor mínimo sobre el que realizar la media para colocar las líneas de separación
    # Salidas: Vectores de coordenadas 'y' de inicio y final de línea
    def filas(self, histograma, umbral):
        long = histograma.size
        inicioFila = []
        finalFila = []
        inicio =[]
        final = []

        # Detectar inicio de la primera fila
        inicioPrimeraFila = 0
        for x in range(0, long - 1):
            if (histograma[x] <= umbral) & (histograma[x] > 0):
                inicioPrimeraFila = x
                break
        # Detectar final de la última fila
        finalUltimaFila = long - 1
        for x in range(long - 1, 0, -1):
            if (histograma[x] <= umbral) & (histograma[x] > 0):
                finalUltimaFila = x
                break
        #Detectar filas
        for x in range(inicioPrimeraFila, finalUltimaFila):
            # Detectar inicio de fila
            if (histograma[x] < umbral) & (histograma[x + 1] >= umbral):
                inicioFila.append(x + 1)
            # Detectar final de fila
            if (histograma[x] >= umbral) & (histograma[x + 1] < umbral):
                finalFila.append(x)

        inicio.append(inicioPrimeraFila)

        numeroFilas = len(inicioFila)
        zeros_ini = np.zeros(numeroFilas)
        zeros_fin = np.zeros(numeroFilas)

        for x in range(0, numeroFilas - 1):
            zeros_fin[x] = finalFila[x]
            zeros_ini[x] = inicioFila[x + 1]

            for y in range(finalFila[x], inicioFila[x + 1]):
                if (histograma[y] == 0) & (histograma[y + 1] > 0):
                    zeros_ini[x] = y + 1

                if (histograma[y] > 0) & (histograma[y + 1] == 0):
                    zeros_fin[x] = y

            if (zeros_ini[x] == inicioFila[x + 1]) & (zeros_fin[x] == finalFila[x]):
                index = np.argmin(histograma[finalFila[x]:inicioFila[x + 1]]) + finalFila[x]
                final.append(index)
                inicio.append(index)
            else:
                final.append(int(zeros_fin[x]))
                inicio.append(int(zeros_ini[x]))

        final.append(finalUltimaFila)

        return (inicio, final)

    # Entrada: Histograma horizontal de la fila
    # Entrada: Valor mínimo sobre el que realizar la media para colocar las líneas de separación
    # Salidas: Vectores de coordenadas 'x' de inicio y final de palabra
    def palabras(self, histograma, minimo_hueco, minimo_palabra):
        long = histograma.size
        ini = []
        fin = []
        inicios = []
        finales = []
        inicios_ok = []
        finales_ok = []

        for x in range(0, long-1):
            if (histograma[x] == 0) & (histograma[x + 1] > 0):
                ini.append(x + 1)

            if (histograma[x] > 0) & (histograma[x + 1] == 0):
                fin.append(x)

        inicios.append(ini[0])

        for x in range(0,len(ini)-1):
            if (ini[x+1]-fin[x]) > minimo_hueco:
                finales.append(fin[x])
                inicios.append(ini[x+1])

        finales.append(fin[len(fin)-1])

        for x in range(0,len(inicios)):
            if finales[x]-inicios[x] > minimo_palabra:
                inicios_ok.append(inicios[x])
                finales_ok.append(finales[x])

        return (inicios_ok,finales_ok)


    def ajustar(self, histograma):
        long = histograma.size

        inicio = 0
        final = 0

        if histograma[0] == 0:
            for x in range(0, long - 1):
                if (histograma[x] == 0) & (histograma[x + 1] > 0):
                    inicio = x + 1
                    break

        if histograma[long-1] == 0:
            for x in range(long - 1, 0, -1):
                if (histograma[x] == 0) & (histograma[x - 1] > 0):
                    final = long - (x - 1)
                    break

        return (inicio, final)

    def ampliar(self, histograma, margen):
        long = histograma.size

        inicio = 0
        final = 0

        if histograma[margen] > 0:
            for x in range(margen - 1, 0, -1):
                if histograma[x] == 0:
                    inicio = margen - x

        if histograma[long - 1 - margen] > 0:
            for x in range(long - margen, long - 1):
                if histograma[x] == 0:
                    final = x - (long - 1 - margen)

        return (inicio, final)

    def borde(self, img):

        img_bw = (img < 1).astype('uint8')

        label = measure.label(img_bw)

        for region in measure.regionprops(label):
            minr, minc, maxr, maxc = region.bbox
            bbox_height = maxr - minr
            bbox_width = maxc - minc
            img_dims = label.shape
            if bbox_height * bbox_width > img_dims[0] * img_dims[1] * 0.4:
                for points in region.coords:
                    img[points[0], points[1]] = 255

        return img