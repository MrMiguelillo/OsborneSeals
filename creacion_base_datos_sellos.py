from FeaturesIO import FeaturesIO as FtIO
import cv2.xfeatures2d as xf
import cv2

path_sellos = 'C:/Users/usuario/Desktop/new_base'

surf = xf.SURF_create()
# orb = cv2.ORB_create()
FtIO.process_and_save(path_sellos, "car_sellos", surf)
