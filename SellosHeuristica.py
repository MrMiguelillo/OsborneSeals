import cv2
import numpy as np
import types


class Sellos:
    @staticmethod
    def test_simetria(bin_img_region):
        # if len(bin_img_region) < 1:
        #     return float('inf')

        fil, col = bin_img_region.shape
        if col <= 1 or fil <=1:
            return float('inf')

        if col % 2 != 0:
            img_right = bin_img_region[0:fil, int(col / 2) + 1:col]
        else:
            img_right = bin_img_region[0:fil, int(col / 2):col]
        img_left = bin_img_region[0:fil, 0:int(col / 2)]

        flip_left_img = cv2.flip(img_left, 1)  # 1 means y axis
        subtracted_img = abs((flip_left_img/255 - img_right/255))*255

        sub_area = np.sum(subtracted_img)
        ref_area = (np.sum(img_left) + np.sum(img_right)) / 2.0

        ratio = sub_area / ref_area

        return ratio

    @staticmethod
    def colision(bbox1, bbox2, min_separacion):
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
                if Sellos.colision(region.bbox, all_other_regions[i].bbox, 4) and region.label != all_other_regions[i].label:
                    for points in all_other_regions[i].coords:
                        label_image[points[0], points[1]] = min(region.label, all_other_regions[i].label)
                    region.label = min(region.label, all_other_regions[i].label)
                    regions[i].label = min(region.label, all_other_regions[i].label)

        return label_image
# TODO: Comprobar qué ordenación tienen los bboxes para ahorrar comprobaciones
# TODO: la búsqueda de colisiones se puede acelerar con matriz de dónde hay rectángulo

    @staticmethod
    def eliminar_borde(regions, label_image):
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
