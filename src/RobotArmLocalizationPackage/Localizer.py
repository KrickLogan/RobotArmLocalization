from math import tan,radians
# from typing import List

from PIL.Image import Image
from DetectedObject import DetectedObject
from ObjectDetector import ObjectDetector
import Utilities.utils as utils
# from inspect import currentframe, getframeinfo
from Vector import Vector

# The Localizer Class holds and provides the rotation which translates
#  a vector to its corresponding position relative to the Robot arm's positioning
#  system.

class Localizer:
    
    def __init__(self):
        self.f_rot_vector = None
        self.f_rot_rads = None
        self.s_rot_vector = None
        self.s_rot_rads = None
        
    def get_real_position(self, t_vector: Vector) -> Vector:
        ''' This Function is the final usage of the system. It applies the rotations to the vector of the detected object
        to get it's position in terms of the positioning systems coordinate system.  
        '''
        t_vector=t_vector.rotate_about_vector(self.f_rot_vector, self.f_rot_rads)
        t_vector=t_vector.rotate_about_vector(self.s_rot_vector, self.s_rot_rads)
        return t_vector
    
    def calibrate(self, cam_claw_1: Vector, pos_claw_1: Vector, cam_claw_2: Vector, pos_claw_2: Vector):
        self.f_rot_vector = cam_claw_1.cross(pos_claw_1)
        self.f_rot_rads = cam_claw_1.angle_between(pos_claw_1)
        self.s_rot_vector = pos_claw_1
        cam_claw_2 = cam_claw_2.rotate_about_vector(self.f_rot_vector.unit(),self.f_rot_rads)
        self.s_rot_rads = cam_claw_2.perp(self.s_rot_vector).angle_between(pos_claw_2.perp(self.s_rot_vector))

