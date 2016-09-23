import numpy as np
import os
import cv2
import cv2.xfeatures2d as xf


def write_features_to_file(filename, locs, desc, shape):
    np.savez(filename, np.hstack((locs, desc)), shape)


def pack_keypoint(keypoints, descriptors, shape):
    kpts = np.array([[kp.pt[0], kp.pt[1], kp.size, kp.angle,
                      kp.response, kp.octave,
                      kp.class_id]
                     for kp in keypoints])
    desc = np.array(descriptors)
    return kpts, desc, shape


def unpack_keypoint(file):
    seals_kps = []
    seals_des = []
    array = file['arr_0']
    for i in range(0, 5):
        kpts = array[i]

        keypoints = [cv2.KeyPoint(x, y, _size, _angle, _response, int(_octave), int(_class_id))
                     for x, y, _size, _angle, _response, _octave, _class_id in list(kpts)]
        seals_kps.append(keypoints)

    for i in range(5, 10):
        desc = np.array(array[i])
        seals_des.append(desc)

    seal_shps = file['arr_1']

    return seals_kps, seals_des, seal_shps


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
            img = cv2.imread(path + curr_file, 0)

            k = detector.detect(img, None)
            if len(k) > 0:
                k, des = detector.compute(img, k)
            else:
                des = []
            k, des, shape = pack_keypoint(k, des, img.shape)  #
            all_k.append(k.tolist())
            all_d.append(des.tolist())
            all_s.append(shape)

    write_features_to_file(resultname, all_k, all_d, all_s)


def load_features(filename):
    file = np.load(filename)
    kp, des, shps = unpack_keypoint(file)
    return kp, des, shps

path_sello = 'C:/Users/usuario/Desktop/Base_sellos/'
img1 = cv2.imread(path_sello + "sello1.png", 0)  # Sello
img2 = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)  # Documento

surf = xf.SURF_create()
process_and_save(path_sello, "car_sellos", surf)

npzfile = np.load('car_sellos.npz')
a = 0
kp1, desc1 = surf.detectAndCompute(img1, None)
kp_saved, desc_saved, shapes = load_features("car_sellos.npz")

diff = desc1 - desc_saved[1]
print(np.linalg.norm(diff))
