import src.EliminacionSellos as ElimSe
import cv2


img = cv2.imread('C:/Users/usuario/Desktop/documentos/1877-L119.M23_Tomas_Osborne_Bohl/3/'
                 '1877-L119.M23_TomasOsborneBohl.I_3/IMG_0001.png', 0)
# img = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/
# 1/1882-L123.M17.I-1/IMG_0002.png', 0)  # trainImage

path = 'C:/Users/usuario/Desktop/Base_sellos/'
elim_sellos = []

for i in range(0, 5):
    elim_sellos.append(ElimSe.EliminacionSellos(img, i))

elim_sellos[0].get_keypoints_from_db('car_sellos.npz')
elim_sellos[0].get_document_features()

real_seal = -1
max_occurrences = 0
for i in range(0, 5):
    elim_sellos[i].get_matched_keypoints()
    elim_sellos[i].compute_evidence_matrix()
    elim_sellos[i].compute_position_and_max_occurrences()
    if elim_sellos[i].max_occurrences > max_occurrences:
        max_occurrences = elim_sellos[i].max_occurrences
        real_seal = i

elim_sellos[real_seal].remove_seal()

cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.imshow('Result', img)
cv2.waitKey()

# TODO: Funciona, falta ver si devuelve el resultado correcto
