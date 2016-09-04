import numpy as np


class SealLocator:
    NUM_DIVISSIONS = 10
    evidence_matrix = np.array([[]])

    def __init__(self, img):
        fils, cols = img.shape
        SealLocator.evidence_matrix.resize((fils / SealLocator.NUM_DIVISSIONS, cols / SealLocator.NUM_DIVISSIONS))

    def calc_occurrences(self, keypoints):
        for kp in keypoints:
            normal = int(kp.pt[0] / SealLocator.NUM_DIVISSIONS, kp.pt[1] / SealLocator.NUM_DIVISSIONS)
            SealLocator.evidence_matrix[]