import cv2
import paths
import SellosHeuristica as Sh
from Database import DatabaseHeur

path = paths.path_to_imgs
img_path = path + '1890-L10.M1/122/IMG_0001.png'
db = DatabaseHeur('docs_osborne', 'testuser', 'test123', 'heur_results1')

documento = Sh.Documento()
documento.load_img(img_path)
documento.get_bin_img()
# documento.apply_img_corrections()
documento.get_lines()
documento.get_regions()

# i = 0
for region in documento.regions:
    region.test.apply_active_tests()
    cv2.rectangle(documento.bin_img, (region.minc, region.minr), (region.maxc, region.maxr), 180, 3)
    cv2.putText(documento.bin_img, str(region.id), (region.minc, region.minr), cv2.FONT_HERSHEY_PLAIN, 3, 180, 3)
# documento.elim_self_contain()

# for seal in documento.seals:
    # cv2.rectangle(documento.bin_img, (seal.minc, seal.minr), (seal.maxc, seal.maxr), 180, 3)
    # cv2.putText(documento.bin_img, str(seal.id), (seal.minc, seal.minr), cv2.FONT_HERSHEY_PLAIN, 3, 180, 3)
    # i += 1
    # region_img = documento.img[region.minr:region.maxr, region.minc:region.maxc]
    # cv2.imwrite(paths.path_to_heur + '/' + str(i) + 'IMG_0003.png', region_img)
    # db.insert_results({"path": img_path.replace("\\", "/")})

cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', documento.bin_img*255)
cv2.waitKey()

# TODO: use np.searchsorted to find row in line separator list of rows:
#   - if region.minr < said value and region.maxr > said value
#      -> reject region (delete from list of regions or whatever)
