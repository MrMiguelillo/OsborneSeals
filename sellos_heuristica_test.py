import cv2
import paths
import SellosHeuristica as Sh
from Database import DatabaseHeur

path = paths.path_to_imgs
img_path = path + '/2016_09_09/181/IMG_0002.png'
db = DatabaseHeur('docs_osborne', 'testuser', 'test123', 'heur_results1')

# doc_img = cv2.imread('C:/Users/usuario/Desktop/documentos/1883-L119.M29_Tomas_Osborne_Born/'
#                  '1/1883-L119.M29_Tomas_Osborne_Born/IMG_0001.png', cv2.IMREAD_GRAYSCALE)

documento = Sh.Documento()
documento.load_img(img_path)
documento.get_bin_img()
documento.apply_img_corrections()
documento.get_regions()

i = 0
for region in documento.regions:
    region.test.apply_active_tests()
    # seals = []
    # if region.region_is_seal:
        # seals.append(region)
    cv2.rectangle(documento.bin_img, (region.minc, region.minr), (region.maxc, region.maxr), 180, 3)
    cv2.putText(documento.bin_img, str(region.id), (region.minc, region.minr), cv2.FONT_HERSHEY_PLAIN, 3, 180, 3)
        # region_img = documento.img[region.minr:region.maxr, region.minc:region.maxc]
        # cv2.imwrite(paths.path_to_heur + '/' + str(i) + 'IMG_0003.png', region_img)
    i += 1
        # db.insert_results({"path": img_path.replace("\\", "/")})

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', documento.bin_img*255)
cv2.waitKey()
