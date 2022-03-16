from fileinput import filename
from logging import FileHandler
from math import tan,radians
import pickle
from typing import List

from PIL.Image import Image
from arm_localizer.detected_object import DetectedObject
from arm_localizer.object_detector import ObjectDetector
import arm_localizer.utilities.utils as utils
# from inspect import currentframe, getframeinfo
from arm_localizer.vector import Vector


# The Localizer Class holds and provides the rotation which translates
#  a vector to its corresponding position relative to the Robot arm's positioning
#  system.

class LocalizerNotInitializedError(Exception):
    pass

class Localizer:
    
    def __init__(self):
        # self.f_rot_vector = None
        # self.f_rot_rads = None
        # self.s_rot_vector = None
        # self.s_rot_rads = None
        # self.rotation = utils.unpickle()  
        filename = "./rotation.pkl"
        fh = open(filename, "rb")
        try:
            fh_new = pickle.load(fh)
        except pickle.UnpicklingError as e:
            print(e)
            raise LocalizerNotInitializedError(f'Unable to load rotation. Need to load rotation to initialize package{filename}.')
        except pickle.PicklingError as e:
            print(e)
            raise LocalizerNotInitializedError(f'Unable to load rotation. Need to load rotation to initialize package{filename}.')
        except (AttributeError,  EOFError, ImportError, IndexError) as e:
            print(e)
            raise LocalizerNotInitializedError(f'Unable to load rotation. Need to load rotation to initialize package{filename}.')
        except Exception as e:
            print(e)
            raise LocalizerNotInitializedError(f'Unable to load rotation. Need to load rotation to initialize package{filename}.')
        else:
            self.rotation = fh_new
        finally:
            fh.close()

        
    def get_real_position(self, t_vector: Vector) -> Vector:
        ''' This Function is the final usage of the system. It applies the rotations to the vector of the detected object
        to get it's position in terms of the positioning systems coordinate system.  
        '''
        t_vector=t_vector.rotate_about_vector(self.rotation._f_rot_vector, self.rotation._f_rot_rads)
        t_vector=t_vector.rotate_about_vector(self.rotation._s_rot_vector, self.rotation._s_rot_rads)
        return t_vector
    
    def calibrate(self, cam_claw_1: Vector, pos_claw_1: Vector, cam_claw_2: Vector, pos_claw_2: Vector):
        self.f_rot_vector = cam_claw_1.cross(pos_claw_1)
        self.f_rot_rads = cam_claw_1.angle_between(pos_claw_1)
        self.s_rot_vector = pos_claw_1
        cam_claw_2 = cam_claw_2.rotate_about_vector(self.f_rot_vector.unit(),self.f_rot_rads)
        self.s_rot_rads = cam_claw_2.perp(self.s_rot_vector).angle_between(pos_claw_2.perp(self.s_rot_vector))
        