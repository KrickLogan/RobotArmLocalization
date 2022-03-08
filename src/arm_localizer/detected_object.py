import string
from typing import Tuple
from matplotlib.pyplot import axis
import numpy as np
from numpy.lib.function_base import average
import torch
import numpy.ma as ma
from .utilities import utils
from math import tan,radians
from .vector import Vector
from scipy.ndimage import center_of_mass


class DetectedObject:

    """This is a detection returned from the model

    A :class:`arm_localizer.detected_object.DetectedObject` is generated for each
    detection from the :class:`arm_localizer.object_detector.ObjectDetector`.
    This class stores the outputs from the RCNN model for a detection. The intention
    of this class is to organize and label the model outputs for manipulation. Included
    here are also relevant methods which use the model outputs.

    Attributes:
        label (int): the label of the detection indicating the class. Can be converted to string using
        box (): The bounding box for the detection as pixel coordinates of the corners of the box
        mask (array): An array of values from 0 to 1 indicating the corresponding pixel's confidence of classification 
        relative to the detection class.
        score() : The confidence the model ascribes to this detection

    """
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
        the center point of the bounding box's pixel. Note that this is the untransformed pixel value
        where y goes top to bottom in the image.

        Args:
        none

        Returns:
            tuple: (X,Y) coordinates of center pixel

        """
        x1, y1, x2, y2 = self.box.detach().numpy()
        x = (x1 + x2)/2
        y = (y1 + y2)/2
        return((x,y))

    def get_center_mass_pixel(self) -> tuple:
        """This function returns the center of mass of a :class:`arm_localizer.detected_object.DetectedObject` as an (X,Y) tuple

        This function uses scipy's center_of_mass function to calculate the (X,Y) pixel coordinates of
        the center point of the detected object's mask. Note that this is the untransformed pixel value
        where y goes top to bottom in the image.

        Args:
        none

        Returns:
            tuple: (X,Y) coordinates of center pixel

        """
        # get the boolean mask and convert it from a tensor to a numpy array
        bool_mask_arr = self.get_bool_mask().numpy()
        
        #convert the boolean mask array into a binary mask array
        binary_mask_arr = bool_mask_arr.astype(int)

        # use scipy's center_of_mass function to calculate the center of mass
        center_mass = center_of_mass(binary_mask_arr)

        # flip (y,x) to (x,y)
        center_mass_pixel = (center_mass[1],center_mass[0])

        return center_mass_pixel

    def get_label(self):
        """Gets the label of the detected object

        Each detection returned from the model includes a label. This method returns that label for this :class:`arm_localizer.detected_object.DetectedObject`
        Note that this is an integer value.
        
        Args:
            none

        Returns:
            int: label int

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
        """Applies the objects bool mask to the depth_arr argument

        Returns a masked array whose values correspond do depth values within the detected object's mask

        Args:
            depth_arr (np.ndarray): an array whose values are depths from a depth camera in mm

        Returns:
            np.ma: Masked array whose values are limited to depth values inside of the mask

        """

        bool_mask = self.get_bool_mask()
        bool_mask = np.logical_and(bool_mask, depth_arr != 0)
        bool_mask = torch.gt(bool_mask, 0) #convert back to boolean
        mx = ma.masked_array(depth_arr, np.invert(bool_mask).long()) 
        return(mx)

    def get_average_depth(self, masked_depth_arr) -> float:
        """Calculates the average of values in a masked array. Removes outliers.

        This function removes 0's and outliers from a masked array, then calculates the average

        Args:
            masked_depth_arr (np.ma): A masked array of depth values

        Returns:
            float: returns the average after outliers have been removed

        """
        mx = self.get_masked_array(masked_depth_arr)
        average_depth = self.remove_depth_outliers(mx)

        return np.ma.MaskedArray.mean(average_depth)
        
    def remove_depth_outliers(self,masked_depth_arr) -> np.ma:
        """Removes outliers from a masked array.

        This function calculates the mean and standard deviation of values in a masked array,
        then removes array values which are not within 3 standard deviations of the mean.

        Args:
            masked_depth_arr (np.ma): Masked array of depth values from depth camera

        Returns:
            np.ma: Description of return value

        """
        mean= np.ma.MaskedArray.mean(masked_depth_arr)
        std= np.ma.MaskedArray.std(masked_depth_arr)
        z = masked_depth_arr [(masked_depth_arr>(mean- 3* std)) & (masked_depth_arr<(mean+3* std))]
        return z

    def to_vector(self, img_dims, depth_arr) -> Vector:
        # Converts the detected object to a position vector
        """Converts the detected object to a position vector using a depth array.

        This function uses a depth array and a detections position in an image to calculate
        its position in 3d coordinates, represented by this vector. Measurements are in mm.

        Args:
            img_size ((int,int)): The dimensions of the image in pixels
            depth_arr (np.ndarray): A depth array which corresponds to the image and the detections

        Returns:
            :class:`arm_localizer.vector.Vector`: returns a vector which points to the object from the camera

        """
        depth = self.get_average_depth(depth_arr)
        
        raw_obj_center_pxl = self.get_center_pixel()
        
        obj_center_pxl = self.normalize_pixel_value(raw_obj_center_pxl, img_dims)
        
        xy_plane_angle, zy_plane_angle = self.get_angles_between_pixels(obj_center_pxl, img_dims)
        
        y = depth
        x = y * tan(radians(xy_plane_angle))
        z = y * tan(radians(zy_plane_angle))
        return Vector(x,y,z)

    def get_angles_between_pixels(self, obj_center_pxl, img_dims) -> Tuple[float,float]:
        # uses the camera's field of vision to calculate the angle between pixels
        """Calculates a pixel's angular offset from the center pixel in x and y directions

        This function calculates a pixel's angular offset from the center pixel in xy and zy directions.
        This is done by finding the difference in pixel value of the object of interest to the center, 
        and using this value and the width or height (x or z) of the entire image dimension to generate
        a ratio. This ratio is applied to the Horizontal Field of View and Vertical Field of View respectively
        to generate the angles.

        Args:
            obj_center_pxl (Tuple[int, int]): This is the center pixel of the detection.
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """

        vertical_fov = utils.get_vfov() # maybe need to rework this
        horiz_fov = utils.get_hfov()

        obj_x, obj_z = obj_center_pxl
        img_width, img_height = img_dims
        xy_plane_angle = (obj_x)*(horiz_fov)/(img_width)
        zy_plane_angle = (obj_z)*(vertical_fov)/(img_height)
        return xy_plane_angle, zy_plane_angle

    def normalize_pixel_value(self, obj_center_pxl, img_dims):
        
        """Translates pixel coordinates so that y axis is standard (bottom to top, low to high) and so origin is moved to image center

        To make more comprehensible, normalize the pixel values. Initially the center pixel of a detection is given
        relative to a traditionally inverted y-axis. Additionally, the coordinate system of the camera uses
        the center pixel of the image as it's origin. This method corrects the inverted y-value, and then calculates 
        the pixel value of the detection as if the center of the image was the origin.

        Args:
            obj_center_pxl (tuple): The untransformed pixel coordinates of the detected object
            img_dims (tuple): The pixel dimensions of the parent image

        Returns:
            tuple: The normalized pixel coordinate of the center of the detection

        """
        img_width, img_height = img_dims
        img_center_pxl = (img_width/2, img_height/2)

        obj_x, obj_y = obj_center_pxl
        obj_center_pxl = (obj_x, img_height - obj_y)
        new_obj_x, new_obj_y = obj_center_pxl

        new_obj_center_pxl = (new_obj_x - img_center_pxl[0], new_obj_y - img_center_pxl[1])
        return new_obj_center_pxl
