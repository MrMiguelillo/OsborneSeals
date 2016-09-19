import os

path = '../../Osborne/BdD'
walk = os.walk(path)

for root, dir, files in walk:
    for curr_file in files:

        if curr_file == '.DS_Store':
            continue

        dividir = curr_file.split('1883-119.M29_18_IMG_0001_')

        nombreNuevo = '1883-L119.M29_18_IMG_0001_%s' % dividir[1]

        pathAntiguo = path + '/' + curr_file
        pathNuevo = path + '/' + nombreNuevo

        os.rename(pathAntiguo, pathNuevo)