import src.EliminacionSellos as ElimSe
import src.EvidenceMatrix as em
import cv2


img = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)  # trainImage

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
    elim_sellos[i].compute_position_and_max_occurrences()
    if elim_sellos[i].max_occurrences > max_occurrences:
        max_occurrences = elim_sellos[i].max_occurrences
        real_seal = i

elim_sellos[real_seal].remove_seal()

colors = [(255, 20, 255),
          (20, 255, 30),
          (10, 10, 10),
          (10, 20, 255),
          (200, 10, 40)]

# for i, el_se in enumerate(elim_sellos):
#     el_se.calc_occurrences(el_se.kp_matched)
#     print(el_se[i].is_this_seal_type())
#     cv2.circle(doc_img, elim_sellos.vect[])

cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.imshow('Result', img)

# TODO: Funciona, falta ver si devuelve el resultado correcto
