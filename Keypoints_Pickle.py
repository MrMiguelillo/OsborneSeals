import numpy as np
import cv2


class KeypointsPickle:
    @staticmethod
    def pickle(keypoints, descriptors):
        i = 0
        temp_array = []
        for point in keypoints:
            temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
            ++i
            temp_array.append(temp)
        return temp_array

    @staticmethod
    def unpickle(array):
        keypoints = []
        descriptors = []
        for point in array:
            temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2],
                                        _response=point[3],
                                        _octave=point[4], _class_id=point[5])
            temp_descriptor = point[6]
            keypoints.append(temp_feature)
            descriptors.append(temp_descriptor)
        return keypoints, np.array(descriptors)

    SEAL_NO_MATCH = 0
    SEAL_IO = 1
    SEAL_AG = 2
    SEAL_TO_RARO = 3
    SEAL_TOMAS = 4
    SEAL_DOBLE_C = 5

    seal_string = ['No Match', 'IO', 'AG', 'TO Raro', 'Tomas', 'Doble C']

    NUM_SELLOS = 5

    NO_MATCH_THRESH = 100