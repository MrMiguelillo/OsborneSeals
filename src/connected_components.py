import cv2
import numpy as np
from skimage import measure
import matplotlib.patches as mpatches

img = cv2.imread('../imgs/1_1.png', cv2.IMREAD_GRAYSCALE)
ret, bin_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# bin_img = (img < ret*1.1).astype('uint8')*255
kernel1 = np.ones((19,19),np.uint8)
kernel2 = np.ones((3,3),np.uint8)
bin_img = cv2.dilate(bin_img, kernel1)
# bin_img = cv2.erode(bin_img, kernel1)
# bin_img = cv2.erode(bin_img, kernel2)
# bin_img = cv2.dilate(bin_img, kernel2)

# se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
# mask = cv2.morphologyEx(img, cv2.MORPH_CLOSE, se1)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

# bin_img *= (mask/255).astype('uint8')

label_image = measure.label(bin_img)

for region in measure.regionprops(label_image):
    # skip small images
    minr, minc, maxr, maxc = region.bbox
    bbox_height = maxr - minr
    bbox_width = maxc - minc
    if bbox_height * bbox_width < 40000:
        continue
    else:
        print(bbox_width*bbox_height)

    # TODO: Check for smaller areas in case we need to merge two small regions and add bigger area filter after that

    if bbox_height/bbox_width < 0.5 or bbox_height/bbox_width > 2:
        continue

    # check for filled area ratio inside bounding box
    fill_area_ratio = float(region.area) / ((maxr - minr)*(maxc - minc))
    if fill_area_ratio < 0.3 or fill_area_ratio > 0.9:  # 0.9 condition just to avoid black margins false positives
        continue
    # else:
        # print('%d %d %d %d' % (minr, minc, maxr, maxc))
        # cv2.namedWindow('test', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('test', bin_img[minr:int((maxr+minr)/2), minc:maxc])
        # cv2.waitKey()
        # cv2.destroyWindow('test')
        # left_half_area = np.sum(bin_img[minr:int((maxr+minr)/2), minc:maxc], dtype=np.float64)
        # right_half_area = np.sum(bin_img[int((maxr+minr)/2)+1:maxr, minc:maxc], dtype=np.float64)  # Coger slice de mitad derecha
        # half_area_ratio = left_half_area/right_half_area
        # if half_area_ratio < 0.9 or half_area_ratio > (1/0.9):  # or left_half_area == 0 or right_half_area == 0:
        #     ratio_string = '%f' % half_area_ratio
        # cent_row, cent_col = region.centroid
        # cv2.putText(bin_img, ratio_string, (int(cent_col), int(cent_row)), cv2.FONT_HERSHEY_COMPLEX, 1, 180, 5)
        # cv2.rectangle(bin_img, (minc, minr), (maxc, maxr), 180, 5)

    if (maxc+minc) % 2 != 0:
        img_right = bin_img[minr:maxr, int((maxc+minc)/2)+1:maxc]
    else:
        img_right = bin_img[minr:maxr, int((maxc+minc)/2):maxc]
    img_left = bin_img[minr:maxr, minc:int((maxc+minc)/2)]

    left_half_area = np.sum(img_left, dtype=np.float64)
    right_half_area = np.sum(img_right, dtype=np.float64)  # Coger slice de mitad derecha

    # if left_half_area > right_half_area * 1.1:
    #     img_right = cv2.dilate(img_right, kernel)
    # elif right_half_area > left_half_area * 1.1:
    #     img_left = cv2.dilate(img_left, kernel)

    flip_img_left = cv2.flip(img_left, 1)  # 1 means 'y' axis
    subtracted_img = abs(flip_img_left - img_right)

    sub_area = np.sum(subtracted_img)
    ref_area = (np.sum(img_left, dtype=np.float64) + np.sum(img_right, dtype=np.float64)) / 2.0

    ratio = sub_area / ref_area

    if ratio > 0.2:
        continue

    # cv2.namedWindow('test', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('test', subtracted_img)
    # cv2.waitKey()
    # cv2.destroyWindow('test')

    ratio_string = '%f' % ratio
    cent_row, cent_col = region.centroid
    print(ratio)
    # print('%f %f %f %f' % (minc, (maxc+minc)/2, minr, maxr))
    cv2.putText(bin_img, ratio_string, (int(cent_col), int(cent_row)), cv2.FONT_HERSHEY_COMPLEX, 1, 180, 5)
    cv2.rectangle(bin_img, (minc,minr), (maxc,maxr), 255, 5)

#cv2.imwrite('bin_img_new_ratio.png', bin_img)
cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', bin_img)
cv2.waitKey()

'''
    TODO:
        1. Filtrar por test de simetría
'''