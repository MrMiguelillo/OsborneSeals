import cv2
import paths
import SellosHeuristica as Sh

path = paths.path_to_imgs
img_path = path + '/1883-L119.M29/11/IMG_0001.png'

# doc_img = cv2.imread('C:/Users/usuario/Desktop/documentos/1883-L119.M29_Tomas_Osborne_Born/'
#                  '1/1883-L119.M29_Tomas_Osborne_Born/IMG_0001.png', cv2.IMREAD_GRAYSCALE)

documento = Sh.Documento()
documento.load_img(img_path)
documento.get_bin_img()
documento.apply_morphology()
documento.get_regions()

for region in documento.regions:
    region_is_seal = True
    if region.test.active_tests.get("area") is True:
        region.test.area()
        region_is_seal *= region.test.passed_tests.get("area")
    if region.test.active_tests.get("aspect_ratio") is True:
        region.test.aspect_ratio()
        region_is_seal *= region.test.passed_tests.get("aspect_ratio")
    if region.test.active_tests.get("filled_area") is True:
        region.test.filled_area_ratio()
        region_is_seal *= region.test.passed_tests.get("filled_area")
    if region.test.active_tests.get("simmetry") is True:
        region.test.simmetry()
        region_is_seal *= region.test.passed_tests.get("simmetry")

    if region_is_seal:
        cv2.rectangle(documento.bin_img, (region.minc, region.minr), (region.maxc, region.maxr), 180, 3)
        # For testing purposes:
        cv2.putText(documento.bin_img, str(region.id), (region.minc, region.minr), cv2.FONT_HERSHEY_PLAIN, 3, 180, 3)

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', documento.bin_img)
cv2.waitKey()

# TODO: convert this into a class
# TODO: SellosHeuristica, sellos_extraccion_heuristica and this repeats a lot of code -> CLEAN
