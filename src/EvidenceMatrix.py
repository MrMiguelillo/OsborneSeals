import numpy as np
import cv2


class EvidenceMatrix:
    DIVISION_SIZE = 10
    SEAL_DIMENSION = 300  # seals are about 300x300px

    def __init__(self, shape):
        fils, cols = shape
        self.evidence_matrix = np.array([])
        self.evidence_matrix.resize((fils / EvidenceMatrix.DIVISION_SIZE, cols / EvidenceMatrix.DIVISION_SIZE))
        self.evidence_matrix.fill(0)
        self.vect = []

    def calc_occurrences(self, keypoints):
        for kp in keypoints:
            # points are x, y instead of rows and columns
            normal = (int(kp.pt[1] / EvidenceMatrix.DIVISION_SIZE), int(kp.pt[0] / EvidenceMatrix.DIVISION_SIZE))
            self.evidence_matrix[normal[0], normal[1]] += 1

    # def calc_position(self):
    #     num_cells = int(EvidenceMatrix.SEAL_DIMENSION / EvidenceMatrix.DIVISION_SIZE)
    #     kernel = np.ones((num_cells, num_cells))
    #
    #     occurrences = cv2.filter2D(self.evidence_matrix, -1, kernel)
    #     max_occurrences = np.amax(occurrences)
    #     max_index = np.where(occurrences == max_occurrences)
    #     avg_index = (np.average(max_index[0]), np.average(max_index[1]))
    #
    #     final_coords = (int(avg_index[0].item()), int(avg_index[1].item()))
    #
    #     return final_coords
    #
    # def is_this_seal_type(self):
    #     a = self.evidence_matrix.reshape(self.evidence_matrix.shape[0] * self.evidence_matrix.shape[1])
    #     b = a.copy()
    #     b.sort()
    #     max5 = b[-5:]
    #     coords = [np.unravel_index(a.tolist().index(max5[i]), self.evidence_matrix.shape) for i in range(0,5)]
    #     coords = np.array(coords)
    #
    #     self.vect = [[coords[0] - coords[1]],
    #                  [coords[1] - coords[2]],
    #                  [coords[2] - coords[3]],
    #                  [coords[3] - coords[4]],
    #                  [coords[4] - coords[0]]]
    #
    #     dist = np.linalg.norm(self.vect, axis=0)
    #
    #     if np.amax(dist) > (self.SEAL_DIMENSION/self.DIVISION_SIZE)*1.1:
    #         return False
    #     else:
    #         return True
