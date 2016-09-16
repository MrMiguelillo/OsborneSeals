import numpy as np
import os
import cv2
import cv2.xfeatures2d as xf


def write_features_to_file(filename, locs, desc):
    np.save(filename, np.hstack((locs, desc)))


def pack_keypoint(keypoints, descriptors):
    kpts = np.array([[kp.pt[0], kp.pt[1], kp.size, kp.angle,
                      kp.response, kp.octave,
                      kp.class_id]
                     for kp in keypoints])
    desc = np.array(descriptors)
    return kpts, desc


def unpack_keypoint(array):
    seals_kps = []
    seals_des = []
    for i in range(0, 5):
        kpts = array[i]

        keypoints = [cv2.KeyPoint(x, y, _size, _angle, _response, int(_octave), int(_class_id))
                     for x, y, _size, _angle, _response, _octave, _class_id in list(kpts)]
        seals_kps.append(keypoints)

    for i in range(5, 10):
        desc = np.array(array[i])
        seals_des.append(desc)

    return seals_kps, seals_des


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
            k, des = pack_keypoint(k, des)  #
            all_k.append(k.tolist())
            all_d.append(des.tolist())

    write_features_to_file(resultname, all_k, all_d)


def load_features(filename):
    array = np.load(filename)
    kp, des = unpack_keypoint(array)
    return kp, des

path_sello = 'C:/Users/usuario/Desktop/Base_sellos/'
img1 = cv2.imread(path_sello + "sello1.png", 0)  # Sello
img2 = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)  # Documento

surf = xf.SURF_create()
# process_and_save(path_sello, "car_sellos", surf)

kp1, desc1 = surf.detectAndCompute(img1, None)
kp_saved, desc_saved = load_features("car_sellos.npy")

diff = desc1 - desc_saved[1]
print(np.linalg.norm(diff))
