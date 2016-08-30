import os
import numpy as np
import cv2.xfeatures2d as xf
import cv2
from src.Sellos import Sellos
from skimage import measure
import pickle
from src.Keypoints_Pickle import KeypointsPickle


NUM_DOCUMENTOS = 27
found_seal = np.empty(NUM_DOCUMENTOS)

path = "C:/Users/usuario/Desktop/documentos"
walk = os.walk(path)
i = 0
for root, dirs, files in walk:
    for curr_file in files:
        if not curr_file.endswith(".png") or curr_file.startswith("."):
            continue

        img = cv2.imread(root + "/" + curr_file, cv2.IMREAD_GRAYSCALE)
        ret, bin_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((11, 11), np.uint8)
        bin_img = cv2.dilate(bin_img, kernel)

        fils, cols = img.shape

        label_image = measure.label(bin_img)
        regions = measure.regionprops(label_image)

        # eliminar borde si hubiese
        new_label_image = Sellos.eliminar_borde(regions, label_image)
        regions = measure.regionprops(new_label_image)
        # TODO: eliminar región de borde de la lista de regiones para acelerar. También hacerlo sólo si se encuentra borde (devolviendo un bool ademas de new_label)

        # unificar regiones que deberían ser conexas reetiquetando convenientemente
        new_label_image = Sellos.reetiquetado(regions, label_image)

        # reextraer propiedades de regiones reetiquetadas
        regions = measure.regionprops(new_label_image)

        for region in regions:
            minr, minc, maxr, maxc = region.bbox
            bbox_height = maxr - minr
            bbox_width = maxc - minc
            cent_row, cent_col = region.centroid

            # eliminar bboxes pequeñas
            if bbox_height * bbox_width <= 40000:
                continue

            # eliminar bboxes demasiado alargadas
            if bbox_height/bbox_width < 0.5 or bbox_height/bbox_width > 2:
                continue

            # eliminar bboxes demasiado vacías de píxeles blancos
            fill_area_ratio = float(region.area) / ((maxr - minr)*(maxc - minc))
            if fill_area_ratio < 0.2 or fill_area_ratio > 0.9:  # 0.9 condition just to avoid black margins false positives
                continue

            # eliminar bboxes con contenido demasiado poco simétrico
            img_sello = bin_img[minr:maxr, minc:maxc]
            ratio = Sellos.test_simetria(img_sello)

            if ratio > 0.25:
                # si la simetría falla, probar con un binarizado que borre MENOS tinta
                orig_region = img[max(0, minr-10):min(fils, maxr+10), max(0, minc-10):min(cols, maxc+10)]
                bin_region_fatter = (orig_region < ret*1.1).astype('uint8')*255
                bin_region_fatter = cv2.dilate(bin_region_fatter, kernel)
                coords = np.array([minr, maxr, minc, maxc])
                cropped_img, new_coords = Sellos.detectar_bbox(bin_region_fatter, coords)

                ratio = Sellos.test_simetria(cropped_img)
                if ratio > 0.25:
                    # si falla de nuevo, probar con un binarizado que borre MÁS tinta
                    bin_region_slimmer = (orig_region < ret * 0.9).astype('uint8') * 255
                    bin_region_slimmer = cv2.dilate(bin_region_slimmer, kernel)
                    cropped_img, new_coords = Sellos.detectar_bbox(bin_region_slimmer, coords)

                    ratio = Sellos.test_simetria(cropped_img)
                    if ratio > 0.25:
                        continue
                    else:
                        minr = new_coords[0]
                        maxr = new_coords[1]
                        minc = new_coords[2]
                        maxc = new_coords[3]
                else:
                    minr = new_coords[0]
                    maxr = new_coords[1]
                    minc = new_coords[2]
                    maxc = new_coords[3]

            # print(root + curr_file)
            # cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
            # cv2.imshow('Imagen', img[minr:maxr, minc:maxc])
            # cv2.waitKey()
            # cv2.destroyWindow('Imagen')
            # cv2.imwrite('C:/Users/usuario/Desktop/Registro_sellos/sello%d.png' % i, img[minr:maxr, minc:maxc])
            # i += 1
