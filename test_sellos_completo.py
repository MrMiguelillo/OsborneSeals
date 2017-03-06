import cv2
import EliminacionSellos as ElimSe
import path_to_imgs

path = path_to_imgs.path_to_imgs
NUM_SEALS_SAVED = 16  # the number of seals found and stored at car_sellos.npz

img = cv2.imread(path + '/2016_09_09/181/IMG_0002.png', 0)
# img = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/'
#                  '1/1882-L123.M17.I-1/IMG_0002.png', 0)  # trainImage

elim_sellos = []

for i in range(0, NUM_SEALS_SAVED):
    elim_sellos.append(ElimSe.EliminacionSellos(img, i))

elim_sellos[0].get_keypoints_from_db('car_sellos.npz')
elim_sellos[0].get_document_features()

real_seal = -1
max_occurrences = 0
for i in range(0, NUM_SEALS_SAVED):
    elim_sellos[i].get_matched_keypoints()
    elim_sellos[i].compute_evidence_matrix()
    elim_sellos[i].compute_position_and_max_ratio()
    print(i)
    print(elim_sellos[i].max_occurrences)
    print(elim_sellos[i].max_occurrences / len(elim_sellos[i].desc_saved[i]))
    if elim_sellos[i].max_occurrences > max_occurrences:
        max_occurrences = elim_sellos[i].max_occurrences
        real_seal = i

print(real_seal)
elim_sellos[real_seal].remove_seal()

cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.imshow('Result', elim_sellos[real_seal].doc_img)
cv2.waitKey()
