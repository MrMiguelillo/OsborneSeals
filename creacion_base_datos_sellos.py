from FeaturesIO import FeaturesIO as FtIO
import cv2.xfeatures2d as xf

path_sellos = 'base_sellos'

surf = xf.SURF_create()
FtIO.process_and_save(path_sellos, "car_sellos", surf)
