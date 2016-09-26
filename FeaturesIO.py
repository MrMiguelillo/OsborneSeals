import numpy as np
import os
import cv2


class FeaturesIO:
    @staticmethod
    def write_features_to_file(filename, locs, desc, shape):
        np.savez(filename, np.hstack((locs, desc)), shape)

    @staticmethod
    def pack_keypoint(keypoints, descriptors, shape):
        kpts = np.array([[kp.pt[0], kp.pt[1], kp.size, kp.angle,
                          kp.response, kp.octave,
                          kp.class_id]
                         for kp in keypoints])
        desc = np.array(descriptors)
        return kpts, desc, shape

    @staticmethod
    def unpack_keypoint(file):
        seals_kps = []
        seals_des = []
        array = file['arr_0']
        num_elements = len(array)
        for i in range(0, int(num_elements/2)):
            kpts = array[i]

            keypoints = [cv2.KeyPoint(x, y, _size, _angle, _response, int(_octave), int(_class_id))
                         for x, y, _size, _angle, _response, _octave, _class_id in list(kpts)]
            seals_kps.append(keypoints)

        for i in range(int(num_elements/2), num_elements):
            desc = np.array(array[i]).astype(np.uint8)
            seals_des.append(desc)

        seal_shps = file['arr_1']

        return seals_kps, seals_des, seal_shps

    @staticmethod
    def process_and_save(path, resultname, detector):
        walk = os.walk(path)
        all_k = []
        all_d = []
        all_s = []
        for root, dirs, files in walk:
            for curr_file in files:
                if not curr_file.endswith(".png"):
                    continue

                # print(curr_file)
                img = cv2.imread(path + '/' + curr_file, 0)

                k = detector.detect(img, None)
                if len(k) > 0:
                    k, des = detector.compute(img, k)
                else:
                    des = []
                k, des, shape = FeaturesIO.pack_keypoint(k, des, img.shape)  #
                all_k.append(k.tolist())
                all_d.append(des.tolist())
                all_s.append(shape)

        FeaturesIO.write_features_to_file(resultname, all_k, all_d, all_s)

    @staticmethod
    def load_features(filename):
        file = np.load(filename)
        kp, des, shps = FeaturesIO.unpack_keypoint(file)
        return kp, des, shps
