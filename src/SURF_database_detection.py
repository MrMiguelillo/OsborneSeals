import numpy as np
import cv2.xfeatures2d as xf
import cv2
import pickle
from src.Keypoints_Pickle import KeypointsPickle


seal_string = KeypointsPickle.seal_string

path = 'C:/Users/usuario/Desktop/Base_sellos/'
keypoints_database = pickle.load(open(path + "keypoints_database.p", "rb"))
kp = []
desc = []

for i in range(0, len(keypoints_database)):
    kp_temp, desc_temp = KeypointsPickle.unpickle(keypoints_database[i])
    kp.append(kp_temp)
    desc.append(desc_temp)

img = cv2.imread('C:/Users/usuario/Desktop/documentos/1882-L123.M17/1/1882-L123.M17.I-1/IMG_0002.png', 0)
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
        if m.distance < 0.8*n.distance:
            good_matches.append(m)

    if len(good_matches) > max_matches:
        max_matches = len(good_matches)
        matched_seal = i+1

    mask = np.ones((1, len(good_matches)))
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=mask,
                       flags=0)

    print(len(good_matches))
    print(KeypointsPickle.seal_string[i+1])
    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

if max_matches < KeypointsPickle.NO_MATCH_THRESH:
    matched_seal = KeypointsPickle.SEAL_NO_MATCH

print(KeypointsPickle.seal_string[matched_seal])


# TODO: Dibujar matches por si se quieren visualizar resultados.
# TODO en otro archivo: Usar keypoints para delimitar zona de sello ----> Hay que eliminar outliers primero

# TODO IMPORTANTE!!: Por algún motivo el resultado usando bbdd de descriptores es distinto de directamente
# Probar comparar en seal_detect_SURF.py y este mismo archivo.
