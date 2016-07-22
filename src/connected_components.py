import cv2
import numpy as np
from skimage import measure
import matplotlib.patches as mpatches

img = cv2.imread('C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/2.png', cv2.IMREAD_GRAYSCALE)
bin_img = (img < 180).astype('uint8')*255

label_image = measure.label(bin_img)

for region in measure.regionprops(label_image):
    # skip small images
    if region.area < 1000:
        continue

    # check for filled area ratio inside bounding box
    minr, minc, maxr, maxc = region.bbox
    fill_area_ratio = float(region.area) / ((maxr - minr)*(maxc - minc))
    if fill_area_ratio < 0.3 or fill_area_ratio > 0.9:  # 0.9 condition just to avoid black margins false positives
        continue
    else:
        print('%d %d %d %d' % (minc, minr, maxc, maxr))
        cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        cv2.imshow('test', bin_img[minc:int((maxc+minc)/2), minr:maxr])
        cv2.waitKey()
        cv2.destroyWindow('test')
        left_half_area = np.sum(bin_img[minc:int((maxc+minc)/2), minr:maxr])
        right_half_area = np.sum(bin_img[int((maxc+minc)/2)+1:maxc, minr:maxr])  # Coger slice de mitad derecha
        #top_half_area = np.sum(bin_img[minc:maxc, minr:(maxr+minr)/2])
        #bot_half_area = np.sum(bin_img[minc:maxc, (maxr+minr)/2 + 1:maxr])
        half_area_ratio = left_half_area/right_half_area
        #if half_area_ratio < 0.97 or half_area_ratio > (1/0.97):
         #   continue

    # draw rectangle around detected regions
    ratio_string = '%f' % half_area_ratio
    cent_row, cent_col = region.centroid
    print(ratio_string)
    cv2.putText(bin_img, ratio_string, (int(cent_col), int(cent_row)), cv2.FONT_HERSHEY_COMPLEX, 1, 180, 5)
    cv2.rectangle(bin_img, (minc,minr), (maxc,maxr), 255, 5)

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', bin_img)
cv2.waitKey()
