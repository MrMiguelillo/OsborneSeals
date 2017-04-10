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
db = DatabaseHeur('docs_osborne', 'testuser', 'test123', 'heur_results1')

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

        i = 0
        for region in documento.regions:
            region_is_seal = True
            region.test.apply_active_tests()
            region_is_seal *= (region.region.test.passed_tests.get("area") *
                               region.region.test.passed_tests.get("aspect_ratio") *
                               region.region.test.passed_tests.get("filled_area") *
                               region.region.test.passed_tests.get("simmetry"))

            if region_is_seal:
                region_img = documento.img[region.minr:region.maxr, region.minc:region.maxc]
                cv2.imwrite(paths.path_to_heur + '/' + i + curr_file, region_img)
                db.insert_results({"path": root.replace("\\", "/")})
                i += 1
