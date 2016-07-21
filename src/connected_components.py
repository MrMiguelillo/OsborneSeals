import cv2
import numpy as np
from skimage import measure
import matplotlib.patches as mpatches

img = cv2.imread('C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/2.png', cv2.IMREAD_GRAYSCALE)
bin_img = (img < 180).astype('uint8')*255
#    fila_ero_bw = img_ero_bw[ini_filas[y]:fin_filas[y], 0:col_px]
label_image = measure.label(bin_img)

for region in measure.regionprops(label_image):
    # skip small images
    if region.area < 1000:
        continue

    # draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    fill_area_ratio = float(region.area) / ((maxr - minr)*(maxc - minc))
    if fill_area_ratio < 0.3 or fill_area_ratio > 0.9:  #0.9 condition just to avoid black margins false positives
        continue

    ratio_string = '%f' % fill_area_ratio
    cent_row, cent_col = region.centroid
    cv2.putText(bin_img, ratio_string, (int(cent_col), int(cent_row)), cv2.FONT_HERSHEY_COMPLEX, 1, 180, 5)
    cv2.rectangle(bin_img, (minc,minr), (maxc,maxr), 255, 5)

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', bin_img)
cv2.waitKey()