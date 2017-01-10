import cv2
import os
from FuncionSellosCompleta import detectar_sello
from Database import Database

path = 'C:/Users/usuario/Desktop/document'
walk = os.walk(path)
db = Database('docs_osborne', 'testuser', 'test123')


for root, dirs, files in walk:
    print(root)
    max_points = 0
    curr_name = ''
    max_coords = (0, 0)
    there_is_any_image = False
    for curr_file in files:
        if curr_file.endswith('.png'):
            there_is_any_image = True
            img = cv2.imread(root + '/' + curr_file, 0)
            img2, coords, nombre, points = detectar_sello(img)
            if points > max_points:
                max_points = points
                curr_name = nombre
                max_coords = coords

    if there_is_any_image:
        # txt_file = open(root + '/result.txt', 'w')
        # txt_file.write(curr_name + '\n')
        # txt_file.write(str(max_coords) + '\n')
        # txt_file.write(str(max_points) + '\n')
        # txt_file.close()

        db.insert_results(root, max_coords, curr_name, max_points)
