import numpy as np
import os
import cv2
import cv2.xfeatures2d as xf


class FeaturesIO:
    @staticmethod
    def write_features_to_file(filename, locs, desc):
        np.save(filename, np.hstack((locs, desc)))

    @staticmethod
    def pack_keypoint(keypoints, descriptors):
        kpts = np.array([[kp.pt[0], kp.pt[1], kp.size, kp.angle,
                          kp.response, kp.octave,
                          kp.class_id]
                         for kp in keypoints])
        desc = np.array(descriptors)
        return kpts, desc

    @staticmethod
    def unpack_keypoint(array):
        seals_kps = []
        seals_des = []
        for i in range(0, 5):
            kpts = array[i]

            keypoints = [cv2.KeyPoint(x, y, _size, _angle, _response, int(_octave), int(_class_id))
                         for x, y, _size, _angle, _response, _octave, _class_id in list(kpts)]
            seals_kps.append(keypoints)

        for i in range(5, 10):
            desc = np.array(array[i]).astype(np.float32)
            seals_des.append(desc)

        return seals_kps, seals_des

    @staticmethod
    def process_and_save(path, resultname, detector):
        walk = os.walk(path)
        all_k = []
        all_d = []
        for root, dirs, files in walk:
            for curr_file in files:
                if not curr_file.endswith(".png"):
                    continue

                # print(curr_file)
                img = cv2.imread(path + curr_file, 0)

                k = detector.detect(img, None)
                if len(k) > 0:
                    k, des = detector.compute(img, k)
                else:
                    des = []
                k, des = FeaturesIO.pack_keypoint(k, des)  #
                all_k.append(k.tolist())
                all_d.append(des.tolist())

        FeaturesIO.write_features_to_file(resultname, all_k, all_d)

    @staticmethod
    def load_features(filename):
        array = np.load(filename)
        kp, des = FeaturesIO.unpack_keypoint(array)
        return kp, des
