import numpy as np
import cv2


class SealLocator:
    NUM_DIVISSIONS = 10
    SEAL_DIMENSION = 300  # seals are about 300x300px
    evidence_matrix = np.array([[]])

    def __init__(self, img):
        fils, cols = img.shape
        self.evidence_matrix.resize((fils / SealLocator.NUM_DIVISSIONS, cols / SealLocator.NUM_DIVISSIONS))
        self.evidence_matrix.fill(0)

    def calc_occurrences(self, keypoints):
        for kp in keypoints:
            # points are x, y instead of rows and columns
            normal = (int(kp.pt[1] / SealLocator.NUM_DIVISSIONS), int(kp.pt[0] / SealLocator.NUM_DIVISSIONS))
            self.evidence_matrix[normal[0], normal[1]] += 1

    def calc_position(self):
        num_cells = int(self.SEAL_DIMENSION / self.NUM_DIVISSIONS)
        kernel = np.ones((num_cells, num_cells))

        occurrences = cv2.filter2D(self.evidence_matrix, -1, kernel)
        max_occurrences = np.amax(occurrences)
        max_index = np.where(occurrences == max_occurrences)
        avg_index = (np.average(max_index[0]), np.average(max_index[1]))

        final_coords = (int(avg_index[0].item()), int(avg_index[1].item()))

        return final_coords

    # def convolution(self):
