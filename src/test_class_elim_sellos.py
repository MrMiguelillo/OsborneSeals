import cv2
import src.EliminacionSellos as ElimSe

img = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)  # trainImage

path = 'C:/Users/usuario/Desktop/Base_sellos/'

elim_sellos = ElimSe.EliminacionSellos(img)
elim_sellos.get_keypoints_from_db('car_sellos.npy')
elim_sellos.get_matched_keypoints()
elim_sellos.detect_position()
seal_name = 'sello%d.png' % elim_sellos.detected_seal
elim_sellos.remove_seal(path + seal_name)

img_sin_sello = elim_sellos.img

cv2.namedWindow('win', cv2.WINDOW_NORMAL)
cv2.imshow('win', img_sin_sello)
cv2.waitKey()
cv2.destroyAllWindows()

