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
documento.apply_img_corrections()
documento.get_regions()

for region in documento.regions:
    region.test.apply_active_tests()

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', documento.bin_img*255)
cv2.waitKey()

# TODO: convert this into a class
# TODO: SellosHeuristica, sellos_extraccion_heuristica and this repeats a lot of code -> CLEAN
