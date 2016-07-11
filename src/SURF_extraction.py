import cv2.xfeatures2d as xf
import cv2
import numpy as np
import pickle


def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
        ++i
        temp_array.append(temp)
    return temp_array


def unpickle_keypoints(array):
    keypoints = []
    descriptors = []
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
                                    octave=point[4], _class_id=point[5])
        temp_descriptor = point[6]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
    return keypoints, np.array(descriptors)


temp_array = []
for i in range(1, 4):
    img_path = 'C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/muestras/%d.png' % i
    img = cv2.imread(img_path, 0)

    surf = xf.SURF_create()
    kp, des = surf.detectAndCompute(img, None)

    temp = pickle_keypoints(kp, des)
    temp_array.append(temp)

pickle.dump(temp_array, open("keypoints_database.p", "wb"))
