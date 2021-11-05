from math import tan,radians
from typing import List

from PIL.Image import Image
from DetectedObject import DetectedObject
from ObjectDetector import ObjectDetector
import Utilities.utils as utils
from inspect import currentframe, getframeinfo
from Vector import Vector

class Localizer:
    def __init__(self, img: Image, depth):
        self.detector = ObjectDetector(img)
        self.detector.run()
        self._image = img
        self._depth_arr = depth
        self.base_vector = Vector #these must be 1 and only 1. should force object detector to error out if more than one of any of these are detected
        self.claw_vector = Vector
        self.object_vector = Vector
        self.target_vector = Vector
        self.rotation_angle = 0
        # self.calculate_vectors()
    #
    # Not ready yet
    # def calibrate_coordinate_system(self, true_claw_position):
    #     truth_vector = Vector(true_claw_positon)
    #     '''
    #     DO ERROR CHECKING FOR THESE AND MORE CONDITIONS SOMEHOW
    #     if self.target_vector.magnitude() != truth_vector.magnitude:
    #         utils.fail(getframeinfo(currentframe))
    #     elif self.target_vector.z != truth_vector.z:
    #         utils.fail(getframeinfo(currentframe))
    #     etc etc for other conditions 
    #     '''
    #     self.rotation_angle = self.target_vector.angle_between(truth_vector)
    #     self.target_vector.xy_rotate(self.rotation_angle)

    def get_claw(self) -> List[DetectedObject]:
        return self.detector.get_claw()
    
    def get_base(self) -> List[DetectedObject]:
        return self.detector.get_base()

    def get_object(self) -> List[DetectedObject]:
        return self.detector.get_object()
    
    def get_target_vector(self) -> Vector:
        #for now will just do the calculations of cl_vec - base_vec. will eventually be handled in vector class
        return Vector(self.claw_vector.x - self.base_vector.x, self.claw_vector.y - self.base_vector.y,
                self.claw_vector.z - self.base_vector.z)
        
    def calculate_vectors(self):
        for detected_object in self.detector.get_detections():
            vector = detected_object.to_vector(self._depth_arr)
            if detected_object.label == utils.BASE_STRING and self.base_vector == None:
                self.base_vectors=vector
            elif detected_object.label == utils.CLAW_STRING and self.claw_vector == None:
                self.claw_vector=vector
            elif detected_object.label == utils.COTTON_STRING and self.object_vector == None:
                self.claw_vectors=vector
            else:
                utils.fail(getframeinfo(currentframe()))

     
    def to_vector(self, detected_object) -> Vector:
        depth = detected_object.get_average_depth(self._depth_arr)
        height, width = self._image.size
        img_center_pxl = (width/2, height/2) #need to fix, y pixels in image are upside down
        obj_center_pxl = detected_object.get_center_pixel()
        vertical_fov = utils.get_vfov()
        horiz_fov = utils.get_hfov()
        xy_plane_angle, zy_plane_angle = self.get_angles_between_pixels(obj_center_pxl, img_center_pxl, vertical_fov, horiz_fov)
        y = depth
        x = y * tan(radians(xy_plane_angle))
        z = y * tan(radians(zy_plane_angle))
        return Vector(x,y,z)

    def get_angles_between_pixels(self, obj_center_pxl, img_center_pxl, vertical_fov, horiz_fov) -> float:
        obj_x, obj_z = obj_center_pxl
        img_x, img_z = img_center_pxl
        xy_plane_angle = (obj_x - img_x)*(horiz_fov/2)/(img_x)
        zy_plane_angle = (obj_z - img_z)*(vertical_fov/2)/(img_z)
        return xy_plane_angle, zy_plane_angle