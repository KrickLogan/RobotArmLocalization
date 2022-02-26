import string
from matplotlib.pyplot import axis
import numpy as np
from numpy.lib.function_base import average
import torch
import numpy.ma as ma
from .utilities import utils
from math import tan,radians
from .vector import Vector



class DetectedObject:
    '''A :class:`arm_localizer.detected_object.DetectedObject` is generated for each
    detection from the :class:`arm_localizer.object_detector.ObjectDetector`.
    This class stores the outputs from the RCNN model for a detection. The intention
    of this class is to organize and label the model outputs for manipulation. Included
    here are also relevant methods which use the model outputs.
    '''
    def __init__(self, label, box, mask, score):
        '''Constructor Method
        '''
        self.label = label
        self.box = box
        self.mask = mask
        self.score = score
    
    def get_center_pixel(self) -> tuple:
        """This function returns the center pixel of the bounding box of a :class:`arm_localizer.detected_object.DetectedObject` as an (X,Y) tuple

        This function uses the bounding box coordinates to calculate the (X,Y) coordinates of
        the center point of the bounding box's pixel.

        Args:
        none

        Returns:
            tuple: (X,Y) coordinates of center pixel

        """
        x1, y1, x2, y2 = self.box.detach().numpy()
        x = (x1 + x2)/2
        y = (y1 + y2)/2
        return((x,y))

    def get_label(self):
        """Gets the label of the detected object

    Each detection returned from the model includes a label. This method returns that label for this :class:`arm_localizer.detected_object.DetectedObject`

    Args:
        none

    Returns:
        string: label string

    """
        return self.label

    def get_bool_mask(self) -> np.ndarray:
        """Returns a boolean array, true values representing a pixel including the detected object, false in pixels without a detected object

        The RCNN Model returns an array called mask which contains values from 0 to 1 which are interpreted
        here as the models certainty that the image contains 

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """   
        bool_mask = self.mask > utils.PRECISION
        # assert bool_mask.ndim == 2
        bool_mask = np.squeeze(bool_mask)
        return bool_mask

    def get_masked_array(self, depth_arr)->np.ma:
        bool_mask = self.get_bool_mask()
        bool_mask = np.logical_and(bool_mask, depth_arr != 0)
        bool_mask = torch.gt(bool_mask, 0) #convert back to boolean
        mx = ma.masked_array(depth_arr, np.invert(bool_mask).long()) 
        return(mx)

    def get_average_depth(self, masked_depth_arr) -> float:
        mx = self.get_masked_array(masked_depth_arr)
        average_depth = self.remove_depth_outliers(mx)

        return np.ma.MaskedArray.mean(average_depth)
        
    def remove_depth_outliers(self,masked_depth_arr) -> np.ma:
        #removing outliers
        mean= np.ma.MaskedArray.mean(masked_depth_arr)
        std= np.ma.MaskedArray.std(masked_depth_arr)
        z = masked_depth_arr [(masked_depth_arr>(mean- 3* std)) & (masked_depth_arr<(mean+3* std))]
        return z

    def to_vector(self, img_size, depth_arr) -> Vector:
        # Converts the detected object to a position vector
        depth = self.get_average_depth(depth_arr)
        width, height = img_size
        img_dims = (width, height)
        img_center_pxl = (width/2, height/2) 
        obj_center_pxl = self.get_center_pixel()
        
        obj_center_pxl = self.normalize_pixel_value(obj_center_pxl, img_center_pxl)
        
        vertical_fov = utils.get_vfov() # maybe need to rework this
        horiz_fov = utils.get_hfov()
        xy_plane_angle, zy_plane_angle = self.get_angles_between_pixels(obj_center_pxl, img_dims, vertical_fov, horiz_fov)
        
        y = depth
        x = y * tan(radians(xy_plane_angle))
        z = y * tan(radians(zy_plane_angle))
        return Vector(x,y,z)

    def get_angles_between_pixels(self, obj_center_pxl, img_dims, vertical_fov, horiz_fov) -> float:
        # uses the camera's field of vision to calculate the angle between pixels
        obj_x, obj_z = obj_center_pxl
        img_width, img_height = img_dims
        xy_plane_angle = (obj_x)*(horiz_fov)/(img_width)
        zy_plane_angle = (obj_z)*(vertical_fov)/(img_height)
        return xy_plane_angle, zy_plane_angle

    def normalize_pixel_value(self, obj_center_pxl, img_center_pxl):
        #translates pixel coordinates so that y axis is standard (bottom to top, low to high) and so origin is moved to image center
        obj_center_pxl = (obj_center_pxl[0], 1080 - obj_center_pxl[1])
        return (obj_center_pxl[0] - img_center_pxl[0], obj_center_pxl[1] - img_center_pxl[1])
