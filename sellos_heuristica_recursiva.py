import os
import numpy as np

import Database
import SellosHeuristica as Sh
import paths

NUM_DOCUMENTOS = 27
found_seal = np.empty(NUM_DOCUMENTOS)

path = paths.path_to_imgs
walk = os.walk(path)
i = 0
for root, dirs, files in walk:
    for curr_file in files:
        if not curr_file.endswith(".png") or curr_file.startswith("."):
            continue
        img_path = root + '/' + curr_file
        documento = Sh.Documento()
        documento.load_img(img_path)
        documento.get_bin_img()
        documento.apply_img_corrections()
        documento.get_regions()

        for region in documento.regions:
            region.test.apply_active_tests()

        # TODO: Agregar resultados a DB  --> Modify DB script to fulfill this task
        # TODO: Guardar imágenes encontradas en paths_to_heur
