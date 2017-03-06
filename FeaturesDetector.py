import cv2.xfeatures2d as xf


def create_detector():
    surf = xf.SURF_create(hessianThreshold=400, upright=True, extended=True)
    return surf