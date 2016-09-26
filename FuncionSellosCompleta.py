import numpy as np
import EliminacionSellos as ElimSe


seal_string = []


def detectar_sello(img):
    elim_sellos = []

    file = np.load('car_sellos.npz')
    num_elements = len(file['arr_1'])
    file.close()

    for i in range(0, num_elements):
        elim_sellos.append(ElimSe.EliminacionSellos(img, i))

    elim_sellos[0].get_keypoints_from_db('car_sellos.npz')
    elim_sellos[0].get_document_features()

    real_seal = -1
    max_occurrences = 0
    for i in range(0, num_elements):
        elim_sellos[i].get_matched_keypoints()
        elim_sellos[i].compute_evidence_matrix()
        elim_sellos[i].compute_position_and_max_occurrences()
        if elim_sellos[i].max_occurrences > max_occurrences:
            max_occurrences = elim_sellos[i].max_occurrences
            real_seal = i

    elim_sellos[real_seal].remove_seal()

    center_coords = elim_sellos[real_seal].position  # (row,col) = (y,x)
    fils, cols = ElimSe.EliminacionSellos.seals_dims[real_seal]
    div_size = elim_sellos[real_seal].evidence_matrix.DIVISION_SIZE

    pt1 = (int(center_coords[1] * div_size - cols / 2), int(center_coords[0] * div_size - fils / 2))
    pt2 = (int(center_coords[1] * div_size + cols / 2), int(center_coords[0] * div_size + fils / 2))

    corner_coords = [pt1, pt2]

    if len(seal_string) < real_seal:
        seal_name = 'Sello no catalogado'
    else:
        seal_name = seal_string[real_seal]

    return elim_sellos[real_seal].doc_img, corner_coords, seal_name
