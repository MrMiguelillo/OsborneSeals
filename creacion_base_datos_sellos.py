from FeaturesIO import FeaturesIO as FtIO
import FeaturesDetector

path_sellos = 'C:/Users/usuario/Desktop/new_base'

surf = FeaturesDetector.create_detector()
FtIO.process_and_save(path_sellos, "car_sellos", surf)
