import numpy as np
import EliminacionSellos as ElimSe

seal_string = ['sello1', 'sello2', 'sello3', 'sello4', 'sello5', 'sello6',
               'sello7', 'sello8', 'sello9', 'sello10', 'sello11', 'sello12']


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
    max_ratio = 0
    for i in range(0, num_elements):
        elim_sellos[i].get_matched_keypoints()
        elim_sellos[i].compute_evidence_matrix()
        elim_sellos[i].compute_position_and_max_ratio()
        if elim_sellos[i].max_occurrences / len(elim_sellos[i].desc_saved[i]) > max_ratio:
            max_ratio = elim_sellos[i].max_occurrences / len(elim_sellos[i].desc_saved[i])
            real_seal = i

        # TODO: Medir cómo cambiar a ratio en lugar de max_ocurrences afecta a los resultados.

    elim_sellos[real_seal].remove_seal()

    center_coords = elim_sellos[real_seal].position  # (row,col) = (y,x)
    real_seal_height, real_seal_width = ElimSe.EliminacionSellos.seals_dims[real_seal]
    div_size = elim_sellos[real_seal].evidence_matrix.DIVISION_SIZE

    pt1 = (int(center_coords[1] * div_size - real_seal_width / 2),
           int(center_coords[0] * div_size - real_seal_height / 2))
    pt2 = (int(center_coords[1] * div_size + real_seal_width / 2),
           int(center_coords[0] * div_size + real_seal_height / 2))

    corner_coords = [pt1, pt2]

    if len(seal_string) < real_seal:
        seal_name = 'Sello no catalogado'
    else:
        seal_name = seal_string[real_seal]

    return elim_sellos[real_seal].doc_img, corner_coords, seal_name, max_ratio
