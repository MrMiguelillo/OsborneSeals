import EliminacionSellos as ElimSe


def detectar_sello(img, num_elements):
    elim_sellos = []

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
        if (elim_sellos[i].max_occurrences / len(elim_sellos[i].desc_saved[i]) > max_ratio and
                elim_sellos[i].position[0] < img.shape[0] / 2):
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

    # if max_ratio < 0.2:  # TODO BIEN GORDO --> GRAFICAR RESULTADOS Y HALLAR ESTE PARÁMETRO
    #     real_seal = -1

    return elim_sellos[real_seal].doc_img, corner_coords, real_seal, max_ratio

if __name__ == '__main__':
    import path_to_imgs
    import numpy as np
    import os
    import cv2

    path = path = path_to_imgs.path_to_imgs
    walk = os.walk(path + '1890-L10.M1/123/')

    file = np.load('car_sellos.npz')
    num_elements = len(file['arr_1'])
    file.close()

    for root, dirs, files in walk:
        max_ratio = 0
        curr_name = ''
        max_coords = ([0, 0], [0, 0])
        there_is_any_image = False
        for curr_file in files:
            if curr_file.endswith('.png'):
                there_is_any_image = True
                img = cv2.imread(root + '/' + curr_file, 0)
                img2, coords, seal_number, ratio = detectar_sello(img, num_elements)
                # TODO: Take keypts import out of that function in order to perform that step only once
                if ratio > max_ratio:
                    max_ratio = ratio
                    # curr_name = seal_string[seal_number]
                    max_coords = coords

    print(max_coords)
    print(seal_number)
    print(ratio)

    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    cv2.imshow('Result', img2)
    cv2.waitKey()
