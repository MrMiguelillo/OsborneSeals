import numpy as np


class EvidenceMatrix:
    DIVISION_SIZE = 10
    SEAL_DIMENSION = 300  # seals are about 300x300px

    def __init__(self, shape):
        fils, cols = shape
        self.evidence_matrix = np.array([])
        self.evidence_matrix.resize((fils / EvidenceMatrix.DIVISION_SIZE, cols / EvidenceMatrix.DIVISION_SIZE))
        self.evidence_matrix.fill(0)

    def calc_occurrences(self, keypoints):
        for kp in keypoints:
            # points are x, y instead of rows and columns
            normal = (int(kp.pt[1] / EvidenceMatrix.DIVISION_SIZE), int(kp.pt[0] / EvidenceMatrix.DIVISION_SIZE))
            self.evidence_matrix[normal[0], normal[1]] += 1
