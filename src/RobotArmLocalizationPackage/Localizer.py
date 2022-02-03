from math import tan,radians
# from typing import List

from PIL.Image import Image
from DetectedObject import DetectedObject
from ObjectDetector import ObjectDetector
import Utilities.utils as utils
# from inspect import currentframe, getframeinfo
from Vector import Vector

# The Localizer Class incudes all functions related to the conversion of
#  data from the detection outputs into real world position values.
#  Using the detector for a list of detections and the depth array from
#  the camera, this class uses the boxes and masks from themodel outputs 
#  in conjunction with the depth array to calculate the position vectors

class Localizer:
    
    def __init__(self):
        self.f_rot_vector = None
        self.f_rot_rads = None
        self.s_rot_vector = None
        self.s_rot_rads = None

    # def __init__(self, detector: ObjectDetector, depth):
        # self._image = img
        # self._depth_arr = depth
        # self.base_vector = Vector #these must be 1 and only 1. should force object detector to error out if more than one of any of these are detected
        # self.claw_vector = Vector
        # self.object_vector = Vector
        # self.target_vector = Vector
        # self.base_to_claw_vector = Vector
        # self.calculate_vectors(detector)
        

        # self.rotation_angle = 0
        # self.rotation_plane_vector = Vector
        # self.translate_system()
        
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

    # def calculate_vectors(self, detector: ObjectDetector):
    #     img_size = detector.get_image_size()
    #     self.claw_vector = self.to_vector(detector.get_claw(), img_size)
    #     self.base_vector = self.to_vector(detector.get_base(), img_size)
    #     self.object_vector = self.to_vector(detector.get_object(), img_size)
    #     self.target_vector = self.object_vector - self.base_vector
    #     self.base_to_claw_vector = self.claw_vector - self.base_vector
    
     
    # def to_vector(self, detected_object: DetectedObject, img_size) -> Vector:
    #     # Converts the detected object to a position vector
    #     depth = detected_object.get_average_depth(self._depth_arr)
    #     width, height = img_size
    #     img_dims = (width, height)
    #     img_center_pxl = (width/2, height/2) 
    #     obj_center_pxl = detected_object.get_center_pixel()
        
    #     obj_center_pxl = self.normalize_pixel_value(obj_center_pxl, img_center_pxl)
        
    #     vertical_fov = utils.get_vfov()
    #     horiz_fov = utils.get_hfov()
    #     xy_plane_angle, zy_plane_angle = self.get_angles_between_pixels(obj_center_pxl, img_dims, vertical_fov, horiz_fov)
        
    #     y = depth
    #     x = y * tan(radians(xy_plane_angle))
    #     z = y * tan(radians(zy_plane_angle))
    #     return Vector(x,y,z)

    # def get_angles_between_pixels(self, obj_center_pxl, img_dims, vertical_fov, horiz_fov) -> float:
    #     # uses the camera's field of vision to calculate the angle between pixels
    #     obj_x, obj_z = obj_center_pxl
    #     img_width, img_height = img_dims
    #     xy_plane_angle = (obj_x)*(horiz_fov)/(img_width)
    #     zy_plane_angle = (obj_z)*(vertical_fov)/(img_height)
    #     return xy_plane_angle, zy_plane_angle

    # def normalize_pixel_value(self, obj_center_pxl, img_center_pxl):
    #     #translates pixel coordinates so that y axis is standard (bottom to top, low to high) and so origin is moved to image center
    #     obj_center_pxl = (obj_center_pxl[0], 1080 - obj_center_pxl[1])
    #     return (obj_center_pxl[0] - img_center_pxl[0], obj_center_pxl[1] - img_center_pxl[1])

    # def translate_system():
        # Apply rotation to the target vector
