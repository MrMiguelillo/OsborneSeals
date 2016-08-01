import cv2
import numpy as np


class Sellos:
    def test_simetria(self, bin_img_region):
        fil, col = bin_img_region.shape
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

    def colision(self, bbox1, bbox2, min_separacion):
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

    def detectar_bbox(self, img_region, coords):
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

        new_coords = np.array([coords[0]+min_fil, coords[1]-(fil-max_fil), coords[2]+min_col, coords[3]-(col-max_col)])

        return img_region[min_fil:max_fil, min_col:max_col], new_coords

    # def unificar_con(self, ):
