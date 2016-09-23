import os
import cv2.xfeatures2d as xf
import cv2
import numpy as np
import pickle
from src.Keypoints_Pickle import KeypointsPickle


temp_array = []
path = "C:/Users/usuario/Desktop/Base_sellos"
walk = os.walk(path)
for root, dirs, files in walk:
    for curr_file in files:
        if curr_file.endswith(".p"):
            continue

        img = cv2.imread(root + "/" + curr_file, cv2.IMREAD_GRAYSCALE)
        print(curr_file)

        surf = xf.SURF_create()
        kp, des = surf.detectAndCompute(img, None)
        print(len(kp))

        temp = KeypointsPickle.pickle(kp, des)
        temp_array.append(temp)

pickle.dump(temp_array, open(path + "/" + "keypoints_database.p", "wb"))
