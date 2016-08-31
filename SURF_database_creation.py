import cv2.xfeatures2d as xf
import cv2
import numpy as np
import pickle
from Keypoints_Pickle import KeypointsPickle


temp_array = []
for i in range(1, 4):
    img_path = 'C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/muestras/%d.png' % i
    img = cv2.imread(img_path, 0)

    surf = xf.SURF_create()
    kp, des = surf.detectAndCompute(img, None)

    temp = KeypointsPickle.pickle(kp, des)
    temp_array.append(temp)

pickle.dump(temp_array, open("keypoints_database.p", "wb"))
