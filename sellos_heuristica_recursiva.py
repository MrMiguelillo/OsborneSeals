import os
import numpy as np
import cv2

from Database import DatabaseHeur
import SellosHeuristica as Sh
import paths

NUM_DOCUMENTOS = 27
found_seal = np.empty(NUM_DOCUMENTOS)

path = paths.path_to_imgs
walk = os.walk(path)
db = DatabaseHeur('docs_osborne', 'testuser', 'test123', 'heur_results2')

i = 0
for root, dirs, files in walk:
    for curr_file in files:
        if not curr_file.endswith(".png") or curr_file.startswith("."):
            continue
        img_path = root + '/' + curr_file
        print(img_path)
        documento = Sh.Documento()
        documento.load_img(img_path)
        documento.get_bin_img()
        documento.apply_img_corrections()
        documento.get_regions()

        for region in documento.regions:
            region.test.apply_active_tests()
        documento.elim_self_contain()

        for seal in documento.seals:
            seal_img = documento.img[seal.minr:seal.maxr, seal.minc:seal.maxc]

            cv2.imwrite(paths.path_to_heur + '/' + str(i) + curr_file, seal_img)
            db.insert_results({
                "path": root.replace("\\", "/"),
                "reg_id": str(i),
            })
            i += 1
