import cv2
import numpy as np
from src import Sellos
from skimage import measure


sellos = Sellos.Sellos()

img = cv2.imread('../imgs/IMG_0001.png', cv2.IMREAD_GRAYSCALE)
ret, bin_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((11, 11), np.uint8)
bin_img = cv2.dilate(bin_img, kernel)

label_image = measure.label(bin_img)
regions = measure.regionprops(label_image)

# unificar regiones que deberían ser conexas reetiquetando convenientemente
colisiones = np.zeros(50, dtype=np.uint8)
for region in regions:
    all_other_regions = regions
    for i in range(1, len(all_other_regions)):
        if sellos.colision(region.bbox, all_other_regions[i].bbox, 6) and region.label != all_other_regions[i].label:
            for points in all_other_regions[i].coords:
                label_image[points[0], points[1]] = min(region.label, all_other_regions[i].label)
            region.label = min(region.label, all_other_regions[i].label)
            regions[i].label = min(region.label, all_other_regions[i].label)
# TODO: Comprobar qué ordenación tienen los bboxes para ahorrar comprobaciones
# TODO: la búsqueda de colisiones se puede acelerar con matriz de dónde hay rectángulo

# reextraer propiedades de regiones reetiquetadas
regions = measure.regionprops(label_image)

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
    ratio = sellos.test_simetria(img_sello)

    if ratio > 0.25:
        # si la simetría falla, probar con un binarizado que borre MENOS tinta
        orig_region = img[minr-10:maxr+10, minc-10:maxc+10]
        bin_region_fatter = (orig_region < ret*1.1).astype('uint8')*255
        bin_region_fatter = cv2.dilate(bin_region_fatter, kernel)
        coords = np.array([minr, maxr, minc, maxc])
        cropped_img, new_coords = sellos.detectar_bbox(bin_region_fatter, coords)
        ratio = sellos.test_simetria(cropped_img)
        print(ratio)
        if ratio > 0.25:
            # si falla de nuevo, probar con un binarizado que borre MÁS tinta
            bin_region_slimmer = (orig_region < ret * 0.9).astype('uint8') * 255
            bin_region_slimmer = cv2.dilate(bin_region_slimmer, kernel)
            cropped_img, new_coords = sellos.detectar_bbox(bin_region_slimmer, coords)
            ratio = sellos.test_simetria(cropped_img)
            print(ratio)
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

    cv2.rectangle(bin_img, (minc,minr), (maxc,maxr), 255, 5)


cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', bin_img)
cv2.waitKey()

