import cv2
import cv2.xfeatures2d as xf
import pickle
from src.Keypoints_Pickle import KeypointsPickle as KeyP


class EliminacionSellos:
    kps = []
    desc = []

    def get_keypoints(self):
        keypoints_database = pickle.load(open("Base_sellos/keypoints_database.p", "rb"))

        for i in range(0, len(keypoints_database)):
            kp_temp, desc_temp = KeyP.unpickle(keypoints_database[i])
            self.kps.append(kp_temp)
            self.desc.append(desc_temp)

    def detect_seal(self, img):
        surf = xf.SURF_create()
        kp_img, des_img = surf.detectAndCompute(img, None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        max_matches = 0
        matched_seal = 0
        for i in range(0, len(self.desc)):
            good_matches = []
            matches = flann.knnMatch(self.desc[i], des_img, k=2)
            for j, (m, n) in enumerate(matches):
                if m.distance < 0.9 * n.distance:
                    good_matches.append(m)

            if len(good_matches) > max_matches:
                max_matches = len(good_matches)
                matched_seal = i + 1

        if max_matches < KeyP.NO_MATCH_THRESH:
            matched_seal = KeyP.SEAL_NO_MATCH

        return matched_seal

