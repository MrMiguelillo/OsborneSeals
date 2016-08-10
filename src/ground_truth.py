import cv2
import numpy as np
from src.Sellos import Sellos
from skimage import measure


detected_coords = []  # list of strings containing coords for each img

for i in range(1, 48):
    current_img_coords = ''
    img_path = 'C:/Users/usuario/Desktop/sellos/' + str(i) + '.png'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    ret, bin_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((11, 11), np.uint8)
    bin_img = cv2.dilate(bin_img, kernel)

    label_image = measure.label(bin_img)
    regions = measure.regionprops(label_image)

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
        if bbox_height * bbox_width < 40000:
            continue

        # eliminar bboxes demasiado alargadas
        if bbox_height/bbox_width < 0.5 or bbox_height/bbox_width > 2:
            continue

        # eliminar bboxes demasiado vacías de píxeles blancos
        fill_area_ratio = float(region.area) / ((maxr - minr)*(maxc - minc))
        if fill_area_ratio < 0.3 or fill_area_ratio > 0.9:  # 0.9 condition just to avoid black margins false positives
            continue

        # eliminar bboxes con contenido demasiado poco simétrico
        img_sello = bin_img[minr:maxr, minc:maxc]
        ratio = Sellos.test_simetria(img_sello)

        if ratio > 0.25:
            # si la simetría falla, probar con un binarizado que borre MENOS tinta
            orig_region = img[minr-10:maxr+10, minc-10:maxc+10]
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

        if current_img_coords != '':
            current_img_coords += '|'
        current_img_coords += str(minr) + ' - ' + str(minc) + ' - ' + str(maxr-minr) + ' - ' + str(maxc - minc)

        cv2.rectangle(bin_img, (minc, minr), (maxc, maxr), 255, 5)
        cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        cv2.imshow('test', bin_img)
        cv2.waitKey()
        cv2.destroyWindow('test')

    print(current_img_coords)
    detected_coords.append(current_img_coords)

# TODO: añadir bucle para probar distintas imágenes
# TODO: exportar coordenadas detectadas
