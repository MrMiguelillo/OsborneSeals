import cv2
import numpy as np
from skimage import measure


class Region:
    settings = {
        "max_area": 40000,
        "max_aspect_ratio": 2,
        "min_filled_area_ratio": 0.2,
        "max_filled_area_ratio": 0.9,
        "simmetry_ratio_thresh": 0.25,
        "simm_recheck_enlargement_px": 10,
        "simm_recheck_thresh": 0.1,  # percentage tweak to original binaryzation threshold
    }

    def __init__(self, document, coords):
        self.minc, self.maxc, self.minr, self.maxr = coords
        self.test = self.Tests(document)

    class Bbox:
        @staticmethod
        def colision(bbox1, bbox2, min_separacion):
            """
            Simple detector de colisiones entre bboxes con una cierta distancia umbral
            :param bbox1: -
            :param bbox2: -
            :param min_separacion: distancia umbral dentro de la cual se considera colisión igualmente
            :return: True -> Colisionan; False -> No colisionan
            """
            a_minr, a_minc, a_maxr, a_maxc = bbox1
            b_minr, b_minc, b_maxr, b_maxc = bbox2

            a_width = a_maxr - a_minr + min_separacion
            a_height = a_maxc - a_minc + min_separacion
            b_width = b_maxr - b_minr + min_separacion
            b_height = b_maxc - b_minc + min_separacion

            a_x = a_minr
            a_y = a_minc
            b_x = b_minr
            b_y = b_minc

            return (a_x <= b_x + b_width and
                    b_x <= a_x + a_width and
                    a_y <= b_y + b_height and
                    b_y <= a_y + a_height)

        @staticmethod
        def reetiquetado(regions, label_image):
            for region in regions:
                all_other_regions = regions
                for i in range(1, len(all_other_regions)):
                    if (Region.Bbox.colision(region.bbox, all_other_regions[i].bbox, 4) and
                       region.label != all_other_regions[i].label):
                        for points in all_other_regions[i].coords:
                            label_image[points[0], points[1]] = min(region.label, all_other_regions[i].label)
                        region.label = min(region.label, all_other_regions[i].label)
                        regions[i].label = min(region.label, all_other_regions[i].label)

            return label_image
    # TODO: Comprobar qué ordenación tienen los bboxes para ahorrar comprobaciones
    # TODO: la búsqueda de colisiones se puede acelerar con matriz de dónde hay rectángulo

        @staticmethod
        def eliminar_borde(regions, label_image):
            """
            Toma la imagen de etiquetas original y si encuentra alguna región con un área mayor del 40% de la imagen
            original, la elimina. Se usa 40% ya que algunas imágenes contienen dos páginas y dicho borde será un 50% aprox.
            De esta forma se garantiza que el borde cumplirá esta condición y se minimiza la posibilidad de eliminar un
            sello por error (es improbable que un sello ocupe más de el 40% de una imagen).
            :param regions: Lista de regiones encontradas
            :param label_image: Imagen de etiquetas
            :return: Imagen de etiquetas con el supuesto borde etiquetado como fondo (0).
            """
            for region in regions:
                minr, minc, maxr, maxc = region.bbox
                bbox_height = maxr - minr
                bbox_width = maxc - minc
                img_dims = label_image.shape
                if bbox_height * bbox_width > img_dims[0] * img_dims[1] * 0.4:
                    for points in region.coords:
                        label_image[points[0], points[1]] = 0

            return label_image

        @staticmethod
        def detectar_bbox(img_region, coords):
            """
            Readapta los bboxes de las regiones que hayan crecido o encogido tras el cambio de threshold
            :param img_region: recorte de la imagen de la región tras crecer o encoger
            :param coords: coordenadas de la img_region en el documento original
            :return: (nuevo recorte de la imagen, coordenadas de su nuevo bbox)
            """
            fil, col = img_region.shape
            min_col = 0
            limit_detect = False
            for i in range(0, col):
                for j in range(0, fil):
                    if img_region[j, i] != 0:
                        min_col = i
                        limit_detect = True
                        break
                if limit_detect:
                    break

            max_col = 0
            limit_detect = False
            for i in range(col-1, -1, -1):
                for j in range(fil-1, -1, -1):
                    if img_region[j, i] != 0:
                        max_col = i
                        limit_detect = True
                        break
                if limit_detect:
                    break

            min_fil = 0
            limit_detect = False
            for i in range(0, fil):
                for j in range(0, col):
                    if img_region[i, j] != 0:
                        min_fil = i
                        limit_detect = True
                        break
                if limit_detect:
                    break

            max_fil = 0
            limit_detect = False
            for i in range(fil-1, -1, -1):
                for j in range(col-1, -1, -1):
                    if img_region[i, j] != 0:
                        max_fil = i
                        limit_detect = True
                        break
                if limit_detect:
                    break

            new_coords = np.array([coords[0] + min_fil, coords[0] + max_fil, coords[2] + min_col, coords[2] + max_col])

            return img_region[min_fil:max_fil, min_col:max_col], new_coords

        # def unificar_con(self, ):

    class Tests:
        active_tests = {
            "area": True,
            "aspect_ratio": True,
            "filled_area": True,
            "simmetry": True,
        }

        def __init__(self, document):
            self.passed_tests = {
                "area": False,
                "aspect_ratio": False,
                "filled_area": False,
                "simmetry": False,
            }
            self.document = document

        def area(self, width, height):
            if width * height <= Region.settings.get("max_area"):
                self.passed_tests.update({"area": False})
            else:
                self.passed_tests.update({"area": True})

        def aspect_ratio(self, width, height):
            if (width / height > Region.settings.get("max_aspect_ratio") or
               height / width < 1 / Region.settings.get("max_aspect_ratio")):
                self.passed_tests.update({"aspect_ratio": False})
            else:
                self.passed_tests.update({"aspect_ratio": False})

        def filled_area_ratio(self, filled_area, width, height):
            ratio = float(filled_area) / (width * height)
            # 0.9 condition just to avoid black regions false positives
            if (ratio < Region.settings.get("min_filled_area_ratio") or
               ratio > Region.settings.get("max_filled_area_ratio")):
                self.passed_tests.update({"filled_area": False})
            else:
                self.passed_tests.update({"filled_area": True})

        @staticmethod
        def simmetry_ratio(bin_seal):
            """
            Medidor de ratio de simetría. Si la imagen tiene un pixel de alto o ancho (es un entero en lugar de un
             array) o menos (es tipo None porque no se ha cargado), devuelve 'inf' para evitar errores en tiempo de
             ejecución. Es importante distinguir entre imágenes con ancho par o impar a la hora de plegarlas sobre sí.
            :param bin_seal: imagen binarizada de la región a testear
            :return: ratio de simetría. NOTA: Cuanto más cerca de 0, más simétrico.
            """
            fil, col = bin_seal.shape
            if col <= 1 or fil <= 1:
                return float('inf')
            # TODO: Tranformar en raise + un error.

            if col % 2 != 0:
                img_right = bin_seal[0:fil, int(col / 2) + 1:col]
            else:
                img_right = bin_seal[0:fil, int(col / 2):col]
            img_left = bin_seal[0:fil, 0:int(col / 2)]

            flip_left_img = cv2.flip(img_left, 1)  # 1 means y axis
            subtracted_img = abs((flip_left_img / 255 - img_right / 255)) * 255

            sub_area = np.sum(subtracted_img)
            ref_area = (np.sum(img_left) + np.sum(img_right)) / 2.0

            ratio = sub_area / ref_area
            return ratio

        def simmetry(self, coords):
            minr = coords[0]
            maxr = coords[1]
            minc = coords[2]
            maxc = coords[3]

            seal_img = self.document.bin_img[minr:maxr, minc:maxc]
            ratio = self.simmetry_ratio(seal_img)

            if ratio < Region.settings.get("simmetry_ratio_thresh"):
                thickness = Region.settings.get("simm_recheck_enlargement_px")
                enlarged_img = self.document.img[minr - thickness:maxr + thickness,
                                                 minc - thickness:maxc + thickness]
                enlarged_img_coords = [minr - thickness, maxr + thickness, minc - thickness, maxc + thickness]

                dark_thresh = self.document.orig_thresh * (1 + Region.settings.get("simm_recheck_thresh"))
                darker_seal_img = (enlarged_img < dark_thresh).astype('uint8') * 255
                darker_seal_img = self.document.morphology(darker_seal_img)
                cropped_img, new_coords = Region.Bbox.detectar_bbox(darker_seal_img, enlarged_img_coords)
                ratio = self.simmetry_ratio(cropped_img)

                if ratio < Region.settings.get("simmetry_ratio_thresh"):
                    light_thresh = self.document.orig_thresh * (1 - Region.settings.get("simm_recheck_thresh"))
                    lighter_seal_img = (enlarged_img < light_thresh).astype('uint8') * 255
                    lighter_seal_img = self.document.morphology(lighter_seal_img)
                    cropped_img, new_coords = Region.Bbox.detectar_bbox(lighter_seal_img, enlarged_img_coords)
                    ratio = self.simmetry_ratio(cropped_img)

                    if ratio < Region.settings.get("simmetry_ratio_thresh"):
                        self.passed_tests.update({"filled_area": False})
                    else:
                        self.passed_tests.update({"filled_area": True})
                        minr = new_coords[0]
                        maxr = new_coords[1]
                        minc = new_coords[2]
                        maxc = new_coords[3]
                else:
                    self.passed_tests.update({"filled_area": True})
                    minr = new_coords[0]
                    maxr = new_coords[1]
                    minc = new_coords[2]
                    maxc = new_coords[3]
            cv2.rectangle(self.document.bin_img, (minc, minr), (maxc, maxr), 180, 3)


class Documento:
    """
    Clase del documento analizado en cuestión. Sólo va a haber una instancia de documento en todo momento.
    """
    img = np.array([])
    path = ""
    bin_img = np.array([])
    bin_thresh = 0
    kernel = np.ones((11, 11), np.uint8)
    label_img = np.array([])
    regions = []

    def load_img(self, path):
        self.path = path
        self.img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

    def binarization(self):
        self.bin_thresh, self.bin_img = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    def morphology(self, img=None):
        if img is None:
            self.bin_img = cv2.dilate(self.bin_img, self.kernel)
            return None
        else:
            return cv2.dilate(img, self.kernel)

    def get_label_img(self):
        self.label_img = measure.label(self.bin_img)

    def get_regions(self):
        self.regions = measure.regionprops(self.label_img)
