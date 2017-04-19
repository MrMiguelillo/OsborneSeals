import cv2
import numpy as np
from skimage import measure


class LineSeparator:
    settings = {
        "min_lin_dist_px": 60
    }

    @staticmethod
    def horiz_proy(bin_img):
        if np.array_equal(bin_img, bin_img.astype(bool)):
            hist = np.sum(bin_img, 1)
        else:
            raise NameError("Image passed to LineSeparator is not binary")

        return hist

    @staticmethod
    def savitzky_golay(y, window_size, order, deriv=0, rate=1):
        """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
        The Savitzky-Golay filter removes high frequency noise from data.
        It has the advantage of preserving the original shape and
        features of the signal better than other types of filtering
        approaches, such as moving averages techniques.
        Parameters
        ----------
        y : array_like, shape (N,)
            the values of the time history of the signal.
        window_size : int
            the length of the window. Must be an odd integer number.
        order : int
            the order of the polynomial used in the filtering.
            Must be less then `window_size` - 1.
        deriv: int
            the order of the derivative to compute (default = 0 means only smoothing)
        Returns
        -------
        ys : ndarray, shape (N)
            the smoothed signal (or it's n-th derivative).
        Notes
        -----
        The Savitzky-Golay is a type of low-pass filter, particularly
        suited for smoothing noisy data. The main idea behind this
        approach is to make for each point a least-square fit with a
        polynomial of high order over a odd-sized window centered at
        the point.
        Examples
        --------
        t = np.linspace(-4, 4, 500)
        y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
        ysg = savitzky_golay(y, window_size=31, order=4)
        import matplotlib.pyplot as plt
        plt.plot(t, y, label='Noisy signal')
        plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
        plt.plot(t, ysg, 'r', label='Filtered signal')
        plt.legend()
        plt.show()
        References
        ----------
        .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
           Data by Simplified Least Squares Procedures. Analytical
           Chemistry, 1964, 36 (8), pp 1627-1639.
        .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
           W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
           Cambridge University Press ISBN-13: 9780521880688
        """
        from math import factorial

        try:
            window_size = np.abs(np.int(window_size))
            order = np.abs(np.int(order))
        except ValueError as msg:
            raise ValueError("window_size and order have to be of type int")
        if window_size % 2 != 1 or window_size < 1:
            raise TypeError("window_size size must be a positive odd number")
        if window_size < order + 2:
            raise TypeError("window_size is too small for the polynomials order")
        order_range = range(order + 1)
        half_window = (window_size - 1) // 2
        # precompute coefficients
        b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
        m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
        # pad the signal at the extremes with
        # values taken from the signal itself
        firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
        lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
        y = np.concatenate((firstvals, y, lastvals))
        return np.convolve(m[::-1], y, mode='valid')

    @staticmethod
    def is_outlier(points, thresh=2.0035):
        """
        Returns a boolean array with True if points are outliers and False 
        otherwise.

        Parameters:
        -----------
            points : An numobservations by numdimensions array of observations
            thresh : The modified z-score to use as a threshold. Observations with
                a modified z-score (based on the median absolute deviation) greater
                than this value will be classified as outliers.

        Returns:
        --------
            mask : A numobservations-length boolean array.

        References:
        ----------
            Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
            Handle Outliers", The ASQC Basic References in Quality Control:
            Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
        """
        if len(points.shape) == 1:
            points = points[:, None]
        median = np.median(points, axis=0)
        diff = np.sum((points - median) ** 2, axis=-1)
        diff = np.sqrt(diff)
        med_abs_deviation = np.median(diff)

        modified_z_score = 0.6745 * diff / med_abs_deviation

        return modified_z_score > thresh

    @staticmethod
    def find_min(a):
        """
        Encontrar el mínimo valor que se encuentre. Si entre mínimo y mínimo hay menos de, digamos 60px, se ignora el
        más grande de los dos, PUNTO.
        :param a: Array to find local minima in.
        :return: Index of local minima in array
        """
        found_mins = []
        # min_val = float('inf')
        # min_i = 0
        # for i, value in enumerate(a):
        #     if value < min_val:
        #         dist = i - min_i
        #         min_val = value
        #         min_i = i
        #         if dist >= LineSeparator.settings.get("min_lin_dist_px"):
        #             found_mins.append((min_i, min_val))
        #     else:
        #         dist = i - min_i
        #         if dist >= int(LineSeparator.settings.get("min_lin_dist_px") / 2):
        #             min_val = float('inf')

        # take those points which are smaller than their immediate neighbours
        is_min = np.r_[True, a[1:] < a[:-1]] & np.r_[a[:-1] < a[1:], True]
        min_points = []
        true_mins = []
        min_dist = LineSeparator.settings.get("min_lin_dist_px")

        for i, value in enumerate(a):
            if is_min[i]:
                min_points.append((i, value))

        min_points.sort(key=lambda p: p[1])  # lambda function tells sort() which number of the tuple to use
        true_mins.append(min_points[0])

        for point in min_points[1:]:
            too_close = False
            for true_min in true_mins:
                dist = abs(point[0] - true_min[0])
                if dist < min_dist:
                    too_close = True

            if not too_close:
                true_mins.append(point)

        return true_mins


class Region:
    settings = {
        "max_area": 40000,
        "max_aspect_ratio": 3,
        "min_filled_area_ratio": 0.2,
        "max_filled_area_ratio": 0.9,
        "simmetry_ratio_thresh": 0.25,
        "simm_recheck_enlargement_px": 10,
        "simm_recheck_thresh": 0.1,  # percentage tweak to original binaryzation threshold
    }

    def __init__(self, document, coords, filled_area, reg_id):
        self.minr, self.minc, self.maxr, self.maxc = coords
        self.filled_area = filled_area
        self.id = reg_id
        self.region_is_seal = False
        self.test = self.Tests(document, self)

    def __eq__(self, other):
        return self.id == other.id

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

            a_x = a_minr + a_width / 2
            a_y = a_minc + a_height / 2
            b_x = b_minr + b_width / 2
            b_y = b_minc + b_height / 2

            return (abs(a_x - b_x) * 2 < a_width + b_width and
                    abs(a_y - b_y) * 2 < a_height + b_height)

        @staticmethod
        def reetiquetado(regions, label_image):
            j = 0
            for region in regions:
                j += 1
                all_other_regions = regions
                for i in range(0, len(all_other_regions)):
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
            original, la elimina. Se usa 40% ya que algunas imágenes contienen dos págs y dicho borde será un 50% aprox.
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

    class Tests:
        active_tests = {
            "area": True,
            "aspect_ratio": True,
            "filled_area": True,
            "simmetry": False,
            "position": True,
        }

        def __init__(self, document, region):
            self.passed_tests = {
                "area": False,
                "aspect_ratio": False,
                "filled_area": False,
                "simmetry": False,
                "position": False,
            }
            self.document = document
            self.region = region

        def area(self):
            width = self.region.maxr - self.region.minr
            height = self.region.maxc - self.region.minc
            if width * height <= Region.settings.get("max_area"):
                self.passed_tests.update({"area": False})
            else:
                self.passed_tests.update({"area": True})

        def aspect_ratio(self):
            width = self.region.maxr - self.region.minr
            height = self.region.maxc - self.region.minc
            if (width / height > Region.settings.get("max_aspect_ratio") or
               height / width > Region.settings.get("max_aspect_ratio")):
                self.passed_tests.update({"aspect_ratio": False})
            else:
                self.passed_tests.update({"aspect_ratio": True})

        def filled_area_ratio(self):
            width = self.region.maxr - self.region.minr
            height = self.region.maxc - self.region.minc
            filled_area = self.region.filled_area
            ratio = float(filled_area) / (width * height)
            # 0.9 condition just to avoid black regions false positives
            if (ratio < Region.settings.get("min_filled_area_ratio") or
               ratio > Region.settings.get("max_filled_area_ratio")):
                self.passed_tests.update({"filled_area": False})
            else:
                self.passed_tests.update({"filled_area": True})

        @staticmethod
        def symmetry_ratio(bin_seal):
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

        def symmetry(self):
            minr = self.region.minr
            maxr = self.region.maxr
            minc = self.region.minc
            maxc = self.region.maxc

            seal_img = self.document.bin_img[minr:maxr, minc:maxc]
            ratio = self.symmetry_ratio(seal_img)

            if ratio < Region.settings.get("simmetry_ratio_thresh"):
                thickness = Region.settings.get("simm_recheck_enlargement_px")
                enlarged_img = self.document.img[abs(minr - thickness):maxr + thickness,
                                                 abs(minc - thickness):maxc + thickness]
                enlarged_img_coords = [minr - thickness, maxr + thickness, minc - thickness, maxc + thickness]

                dark_thresh = self.document.bin_thresh * (1 + Region.settings.get("simm_recheck_thresh"))
                darker_seal_img = (enlarged_img < dark_thresh).astype('uint8') * 255
                darker_seal_img = self.document.apply_img_corrections(darker_seal_img)
                cropped_img, new_coords = Region.Bbox.detectar_bbox(darker_seal_img, enlarged_img_coords)
                ratio = self.symmetry_ratio(cropped_img)

                if ratio < Region.settings.get("simmetry_ratio_thresh"):
                    light_thresh = self.document.bin_thresh * (1 - Region.settings.get("simm_recheck_thresh"))
                    lighter_seal_img = (enlarged_img < light_thresh).astype('uint8') * 255
                    lighter_seal_img = self.document.apply_img_corrections(lighter_seal_img)
                    cropped_img, new_coords = Region.Bbox.detectar_bbox(lighter_seal_img, enlarged_img_coords)
                    ratio = self.symmetry_ratio(cropped_img)

                    if ratio < Region.settings.get("simmetry_ratio_thresh"):
                        self.passed_tests.update({"filled_area": False})
                    else:
                        self.passed_tests.update({"filled_area": True})
                        self.region.minr = new_coords[0]
                        self.region.maxr = new_coords[1]
                        self.region.minc = new_coords[2]
                        self.region.maxc = new_coords[3]
                else:
                    self.passed_tests.update({"filled_area": True})
                    self.region.minr = new_coords[0]
                    self.region.maxr = new_coords[1]
                    self.region.minc = new_coords[2]
                    self.region.maxc = new_coords[3]

        def position(self):
            height = (self.region.maxr + self.region.minr) / 2

            docr = self.document.img.shape[0]

            if height > docr / 2:
                self.passed_tests.update({"position": False})
            else:
                self.passed_tests.update({"position": True})

        def apply_active_tests(self):
            """
            Applies whichever test might be active and updates region_is_seal accordingly. If it is, it gets added to
            seals list.
            """
            self.region.region_is_seal = True
            if self.region.test.active_tests.get("area") is True:
                self.region.test.area()
                self.region.region_is_seal *= self.region.test.passed_tests.get("area")
            if self.region.test.active_tests.get("aspect_ratio") is True:
                self.region.test.aspect_ratio()
                self.region.region_is_seal *= self.region.test.passed_tests.get("aspect_ratio")
            if self.region.test.active_tests.get("filled_area") is True:
                self.region.test.filled_area_ratio()
                self.region.region_is_seal *= self.region.test.passed_tests.get("filled_area")
            if self.region.test.active_tests.get("simmetry") is True:
                self.region.test.symmetry()
                self.region.region_is_seal *= self.region.test.passed_tests.get("simmetry")
            if self.region.test.active_tests.get("position") is True:
                self.region.test.position()
                self.region.region_is_seal *= self.region.test.passed_tests.get("position")

            if self.region.region_is_seal:
                self.document.seals.append(self.region)


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
    seals = []

    def __init__(self):
        del self.regions[:]
        del self.seals[:]

    def load_img(self, path):
        self.path = path
        self.img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

    def get_bin_img(self):
        self.img = cv2.GaussianBlur(self.img, (3, 3), 0)
        self.bin_thresh, self.bin_img = cv2.threshold(self.img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    def apply_img_corrections(self, img=None):
        if img is None:
            self.bin_img = cv2.GaussianBlur(self.bin_img, (29, 29), 0)
            se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
            se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
            mask = cv2.morphologyEx(self.bin_img, cv2.MORPH_CLOSE, se1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

            out = self.img * mask
            self.bin_img = (out > 5).astype('uint8')
        else:
            aux_img = cv2.GaussianBlur(img, (29, 29), 0)
            se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
            se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
            mask = cv2.morphologyEx(aux_img, cv2.MORPH_CLOSE, se1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

            out = self.img * mask

            return (out > 5).astype('uint8')

    def get_regions(self):
        aux_label_img = measure.label(self.bin_img)
        regs = measure.regionprops(aux_label_img)
        aux_label_img = Region.Bbox.eliminar_borde(regions=regs, label_image=aux_label_img)
        regs = measure.regionprops(aux_label_img)

        self.label_img = Region.Bbox.reetiquetado(regs, aux_label_img)
        regs = measure.regionprops(self.label_img)
        i = 0
        del self.regions[:]
        for reg in regs:
            self.regions.append(Region(self, reg.bbox, reg.area, i))
            i += 1

    def elim_self_contain(self):
        for seal in self.seals:
            seal_bbox = (seal.minr, seal.minc, seal.maxr, seal.maxc)
            j = 0
            while j < len(self.seals):
                bbox2 = (self.seals[j].minr, self.seals[j].minc, self.seals[j].maxr, self.seals[j].maxc)
                if Region.Bbox.colision(seal_bbox, bbox2, 4) and seal != self.seals[j]:
                    self.regions[seal.id].minr = self.seals[j].minr = min(seal.minr, self.seals[j].minr)
                    self.regions[seal.id].minc = self.seals[j].minc = min(seal.minc, self.seals[j].minc)
                    self.regions[seal.id].maxr = self.seals[j].maxr = max(seal.maxr, self.seals[j].maxr)
                    self.regions[seal.id].maxc = self.seals[j].maxc = max(seal.maxc, self.seals[j].maxc)
                    self.regions[seal.id].filled_area = self.seals[j].filled_area =\
                        seal.filled_area + self.seals[j].filled_area
                    del self.seals[j]
                j += 1

# TODO: Make collision distance a parameter at "settings"
