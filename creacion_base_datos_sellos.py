from FeaturesIO import FeaturesIO as FtIO
import FeaturesDetector
import paths

path = paths.path_to_prototypes

surf = FeaturesDetector.create_detector()
FtIO.process_and_save(path, "car_sellos", surf)
