import numpy as np
import cv2.xfeatures2d as xf
import cv2
import pickle


def unpickle_keypoints(array):
    keypoints = []
    descriptors = []
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
                                    _octave=point[4], _class_id=point[5])
        temp_descriptor = point[6]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
    return keypoints, np.array(descriptors)


SEAL_NO_MATCH = 0
SEAL_TOMAS = 1
SEAL_AG = 2
SEAL_DOBLE_T = 3

NUM_SELLOS = 3

keypoints_database = pickle.load(open("keypoints_database.p", "rb"))
kp = []
desc = []

for i in range(0, len(keypoints_database)):
    kp_temp, desc_temp = unpickle_keypoints(keypoints_database[i])
    kp.append(kp_temp)
    desc.append(desc_temp)

img = cv2.imread('C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos/2.png', 0)
surf = xf.SURF_create()
kp_img, des_img = surf.detectAndCompute(img, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

max_matches = 0
matched_seal = 0
for i in range(0, len(keypoints_database)):
    good_matches = []
    matches = flann.knnMatch(desc[i], des_img, k=2)
    for j, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            good_matches.append(m)

    print(len(good_matches))
    if len(good_matches) > max_matches:
        max_matches = len(good_matches)
        matched_seal = i+1

    mask = np.ones(1, len(good_matches))
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=mask,
                       flags=0)

    #img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

if max_matches < 150:
    matched_seal = SEAL_NO_MATCH

print(matched_seal)

# TODO: Dibujar matches por si se quieren visualizar resultados.
# TODO en otro archivo: Usar keypoints para delimitar zona de sello ----> Hay que eliminar outliers primero
