import cv2
import cv2.xfeatures2d as xf
import numpy as np
import src.EvidenceMatrix as em
from src.FeaturesIO import FeaturesIO


class EliminacionSellos:
    doc_img = 0
    doc_kps = []
    doc_des = []
    kps_saved = []
    desc_saved = []
    seals_dims = []

    def __init__(self, img, index):
        EliminacionSellos.doc_img = img
        self.kp_matched = []
        self.evidence_matrix = em.EvidenceMatrix(img.shape)
        self.position = (0, 0)  # position is (rows, cols), therefore, (y, x)
        self.max_occurrences = 0
        self.index = index
        # self.seal_dims = (0, 0)
        # self.detected_seal = 0
        # self.vect = []

    def get_keypoints_from_db(self, path):
        EliminacionSellos.kps_saved, EliminacionSellos.desc_saved, EliminacionSellos.seals_dims\
            = FeaturesIO.load_features(path)

    def get_document_features(self):
        surf = xf.SURF_create()
        EliminacionSellos.doc_kps, EliminacionSellos.doc_des = surf.detectAndCompute(EliminacionSellos.doc_img, None)

    def get_matched_keypoints(self):
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        aux_kp = []
        matches = flann.knnMatch(EliminacionSellos.desc_saved[self.index], EliminacionSellos.doc_des, k=2)
        for j, (m, n) in enumerate(matches):
            if m.distance < 0.9 * n.distance:
                aux_kp.append(EliminacionSellos.doc_kps[m.trainIdx])

        self.kp_matched = aux_kp

    def compute_evidence_matrix(self):
        self.evidence_matrix.calc_occurrences(self.kp_matched)

    def compute_position_and_max_occurrences(self):
        num_cells = int(self.evidence_matrix.SEAL_DIMENSION / self.evidence_matrix.DIVISION_SIZE)
        kernel = np.ones((num_cells, num_cells))

        occurrences = cv2.filter2D(self.evidence_matrix.evidence_matrix, -1, kernel)
        self.max_occurrences = np.amax(occurrences)
        max_index = np.where(occurrences == self.max_occurrences)
        avg_index = (np.average(max_index[0]), np.average(max_index[1]))

        final_coords = (int(avg_index[0].item()), int(avg_index[1].item()))

        self.position = final_coords * self.evidence_matrix.DIVISION_SIZE

    def remove_seal(self):
        div_size = self.evidence_matrix.DIVISION_SIZE
        # seal_img = cv2.imread(path, 0)
        fils, cols = EliminacionSellos.seals_dims[self.index]
        pt1 = (int(self.position[1] * div_size - cols / 2), int(self.position[0] * div_size - fils / 2))
        pt2 = (int(self.position[1] * div_size + cols / 2), int(self.position[0] * div_size + fils / 2))
        cv2.rectangle(EliminacionSellos.doc_img, pt1, pt2, (255, 255, 255), -1)
