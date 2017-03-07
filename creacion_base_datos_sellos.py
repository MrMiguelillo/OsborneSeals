from FeaturesIO import FeaturesIO as FtIO
import FeaturesDetector
import paths

a = paths.path_to_imgs
path_sellos = 'C:/Users/usuario/Desktop/new_base'

surf = FeaturesDetector.create_detector()
FtIO.process_and_save(path_sellos, "car_sellos", surf)
