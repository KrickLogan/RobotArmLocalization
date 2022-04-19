from typing import List
from torchvision.transforms import functional as F
from arm_localizer.utilities import utils, visualizer
from PIL import Image
import numpy as np
from math import sqrt, radians, cos, sin, acos, tan
from scipy.ndimage import center_of_mass
import torch
import numpy.ma as ma
import pickle
import pyrealsense2 as rs

class Vector:
    """This class stores and handles all vector manipulations

    In this system, positions are represented as Vectors. this class supports this class and provides all the relevant operations to do 
    the calculations.

    Attribures:
        x(int): the x value
        y(int): the y value
        z(int): the z value
        

    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """Adds the components of two vectors together

        Args:
            other (Vector): The right hand vector

        Returns:
            Vector: the summed vector

        """
        newx = self.x + other.x
        newy = self.y + other.y
        newz = self.z + other.z
        return Vector(newx, newy, newz)

    def __sub__(self, other):
        """Overload subtraction operator. Subtracts the right hand vector from the left

        Args:
            other (Vector): the right hand vector to be subtracted from the left

        Returns:
            Vector: the result of the subtraction

        """
        newx = self.x - other.x
        newy = self.y - other.y
        newz = self.z - other.z
        return Vector(newx, newy, newz)

    def __mul__(self, c:float):
        """Overload multiplication operator. Scalar multiplication of a vector

        Args:
            c (float): the scalar value to be applied to the vector

        Returns:
            Vector: the result of the multiplication

        """
        return Vector(c*self.x, c*self.y, c*self.z)

    def __truediv__(self, c):
        """Overload division operator. scalar division of a vector

        Args:
            c (Vector): the scalar value to be applied to the vector

        Returns:
            Vector: the result of the division

        """
        return Vector(self.x/c, self.y/c, self.z/c)

    def magnitude(self) -> float :
        """Gets the magnitude of the vector

        calculates the euclidean distance of the vectors and returns it

        Args:
            none

        Returns:
            float: returns the magnitude of the vector

        """
        mag = sqrt((self.x * self.x + self.y * self.y + self.z * self.z))
        return mag

    def dot(self, other) -> float :
        """Dot product of two vectors

        Calculates the Dot product between two vectors

        Args:
            other(Vector): the other vector for the dot product operation

        Returns:
            float: The result of the dot product operation

        """
        dot = self.x * other.x + self.y * other.y + self.z * other.z
        return dot
    
    def rotate_about_vector(self, vNorm, angle:float):
        """Rotates the self vector about the submitted vector by 'angle' radians

        rotates a vector about a different vector by a certain angle

        Args:
            vNorm (Vector): The vector normal to the plane of rotation
            angle (float): the angle of rotation in radians

        Returns:
            Vector: the rotated vector

        """
        vNorm=vNorm.unit()#just in case
        a = self * cos(angle) 
        b = vNorm.cross(self)*sin(angle) 
        c = vNorm * (vNorm.dot(self)) * (1-cos(angle))
        vrot = a + b + c
        return vrot

    def cross(self, other):
        """Cross product of two vectors

        applies the cross product operation between two vectors. the 'other' vector argument is the right
        hand vector for the ooperation

        Args:
            other(Vector): The right hand vector for the cross product operation

        Returns:
            Vector: the result of the cross product operation

        """
        i = Vector(1, 0, 0)
        j = Vector(0, 1, 0)
        k = Vector(0, 0, 1)

        cp = i*(self.y*other.z - other.y*self.z) +  j*(self.z*other.x - self.x*other.z) + k*(self.x*other.y - other.x*self.y)

        return cp


    def angle_between(self, other) -> float:
        """Finds the angle between to vectors

        returns the smallest angle between two vectors. This is unsigned

        Args:
            other(Vector): the othe Vector

        Returns:
            float: returns the angle between the two vectors

        """
        angle = acos(self.dot(other)/(self.magnitude() * other.magnitude()))
        return angle

    def decompose(self):
        i = Vector(self.x, 0, 0)
        j = Vector(0, self.y, 0)
        k = Vector(0, 0, self.z)
        return i, j, k
    
    def project(self, target):
        """Projects the self vector onto the target vector

        Finds the component of the self vector which is parallel to the target vector

        Args:
            target(Vector): The Vector onto which this vector will be projected

        Returns:
            Vector: The component of the self vector which is parallel to the target vector

        """
        proj = target*(self.dot(target)/(target.magnitude()*target.magnitude()))
        return proj

    def perp(self, u):
        """Finds the component of the self vector which is perpendicular to u

        Args:
            u(Vector): the vector

        Returns:
            Vector: The component of the self vector which is perpendicular to the u vector

        """
        return self - self.project(u)

    def as_point(self) -> tuple:
        """Gets the vector as a tuple of 3 values, (x,y,z)

        Args:
            none

        Returns:
            tuple: a set containing the x,y,z coordinates of a vector

        """
        return (self.x, self.y, self.z)
    
    def unit(self):
        """Gets a unit vector parallel to the self vector

        Args:
            none

        Returns:
            Vector: A vector with length 1 which is parallel with the self vector

        """
        return self/self.magnitude()

    def __str__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
        
    def __repr__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
    

class Rotation:
    """This class contains all of the relevant data, as rotations, for the conversion between coordinate systems

    This class consists of two rotations, each composed of a radian value, and a vector of rotation(a vector normal to the plane of rotation)  

    Attribures:
        _f_rot_vector(Vector): The rotation vector for the first rotation
        _f_rot_rads(float): The radian value for the first rotation
        _s_rot_vector(Vector): The rotation vector for the second rotation
        _s_rot_rads(float): The radian value for the second rotation

    """
    def __init__(self, f_rot_vector, f_rot_rads, s_rot_vectors, s_rot_rads):
        self._f_rot_vector = f_rot_vector
        self._f_rot_rads= f_rot_rads
        self._s_rot_vector = s_rot_vectors
        self._s_rot_rads = s_rot_rads

    def set_first_rot_vector(self, f_rot_vector):
        self._f_rot_vector=f_rot_vector
    
    def get_first_rot_vector(self):
        return self._f_rot_vector

    def set_first_rot_radian(self, f_rot_rads):
        self._f_rot_rads=f_rot_rads
    
    def get_first_rot_radian(self):
        return self._f_rot_rads
    
    def set_second_rot_vector(self, s_rot_vector):
        self._s_rot_vector=s_rot_vector
    
    def get_second_rot_vector(self):
        return self._s_rot_vector
    
    def set_second_rot_radian(self, s_rot_rads):
        self._s_rot_rads=s_rot_rads
    
    def get_second_rot_radian(self):
        return self._s_rot_rads


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
        threshold(float): The Threshold value used for determining the level of confidence to use when determining the bool mask.

    """
    def __init__(self, label, box, mask, score, threshold = 0.5):
        '''Constructor Method
        '''
        self.label = label
        self.box = box
        self.mask = mask
        self.score = score
        self.threshold = threshold
    
    def set_threshold(self, new_threshold):
        """Sets the value of threshold.

        Sets the value of the threshold variable. The value of threshold
        must be between 0 and 1.

        Args:
            new_threshold: The new value for threshold, must be between 0 and 1.

        Returns:
            None

        """
        if new_threshold > 0 and new_threshold < 1:
            self.threshold = new_threshold
        else:
            print('Threshold value must be between 0 and 1.')

    def get_threshold(self) -> float:
        """Gets the value of threshold.

        Gets the value of the threshold variable.

        Args:
            None

        Returns:
            threshold(float): The Threshold value used for determining the level of confidence
            to use when determining the bool mask.

        """
        return self.threshold
    
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
        
        # convert the boolean mask array into a binary mask array
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
        bool_mask = self.mask > self.threshold
        # assert bool_mask.ndim == 2
        bool_mask = np.squeeze(bool_mask)
        return bool_mask

    def get_masked_depth_array(self, depth_arr)->np.ma:
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

    def get_average_depth(self, depth_arr) -> float:
        """Calculates the average of values in a masked array. Removes outliers.

        This function removes 0's and outliers from a masked array, then calculates the average

        Args:
            depth_arr (np.ndarray): An array of depth values(mm)

        Returns:
            float: returns the average after outliers have been removed

        """
        mx = self.get_masked_depth_array(depth_arr)
        masked_array_no_outliers = self.remove_depth_outliers(mx)
        # data_labels, data_values = visualizer.get_graph_labels_values(masked_array_no_outliers)
        # visualizer.show_bar_graph(data_labels, data_values, "Depth distribution", "Depth Ranges", "count")
        return np.ma.MaskedArray.mean(masked_array_no_outliers)
        # depth = np.percentile(masked_array_no_outliers.compressed(), 90)
        # print("max: ", masked_array_no_outliers.max())
        # print("min: ", masked_array_no_outliers.min())
        # print(depth)
        return depth
        
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

    def rs_to_vector(self, depth_arr) -> Vector:
        """Converts the detected object to a position vector using a depth array.

        This function uses pyrealsense2's deprojection method, which factors in the camera's intrinsics,
        to calculate its position in 3d coordinates, represented by this vector. Measurements are in mm.

        Args:
            depth_arr (np.ndarray): A depth array which corresponds to the image and the detections

        Returns:
            :class:`arm_localizer.vector.Vector`: returns a vector which points to the object from the camera

        """
        _intrinsics = rs.intrinsics()
        _intrinsics.width = 640
        _intrinsics.height = 480
        _intrinsics.ppx = 324.5739440917969
        _intrinsics.ppy = 243.86447143554688
        _intrinsics.fx = 603.4510498046875
        _intrinsics.fy = 603.4326171875
        _intrinsics.model  = rs.distortion.none
        _intrinsics.coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]

        center_point = self.get_center_mass_pixel()
        average_depth = self.get_average_depth(self.get_masked_depth_array(depth_arr))

        result = rs.rs2_deproject_pixel_to_point(_intrinsics, center_point, average_depth)
        result_vector = Vector(result[0], result[2], -result[1])

        return result_vector

    def to_vector(self, img_size, depth_arr) -> Vector:
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
        
        obj_center_pxl = self.normalize_pixel_value(raw_obj_center_pxl, img_size)
        
        xy_plane_angle, zy_plane_angle = self.get_angles_between_pixels(obj_center_pxl, img_size)
        
        y = depth
        x = y * tan(radians(xy_plane_angle))
        z = y * tan(radians(zy_plane_angle))
        return Vector(x,y,z)

    def get_angles_between_pixels(self, obj_center_pxl, img_dims):
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


class ObjectDetector:
    """This class uses the trained RCNN Model to make detections on an image. It handles the output of the model.

    This class provides an interface for the detections yielded from the model. It can provide the full output
    from the model, or processed individual detections from the model in the form of :class:`arm_localizer.detected_object.DetectedObject` 's

    Attributes:
        _img (PIL.Image): Will be changed
        _model (): The trained model
        _output (): the output of the model as a multi-dimensional array
        claw : won't be here much longer
        base: same
        object: same
    """
    def __init__(self, threshold_claw = 0.5, threshold_base = 0.5, threshold_object = 0.5):
        """Constructor method
        """
        self._output = None
        self._detections = None
        self._claw=None
        self._base=None
        self._object=None

        # Ensure threshold_claw is between 0 and 1
        if threshold_claw > 0 and threshold_claw < 1:
            self.threshold_claw = threshold_claw
        else:
            print('\nClaw Threshold value must be between 0 and 1.\nDefaulting to 0.5.')
            self.threshold_claw = 0.5
        
        # Ensure threshold_base is between 0 and 1
        if threshold_base > 0 and threshold_base < 1:
            self.threshold_base = threshold_base
        else:
            print('\nBase Threshold value must be between 0 and 1.\nDefaulting to 0.5.')
            self.threshold_base = 0.5
        
        # Ensure threshold_object is between 0 and 1
        if threshold_object > 0 and threshold_object < 1:
            self.threshold_object = threshold_object
        else:
            print('\nObject Threshold value must be between 0 and 1.\nDefaulting to 0.5.\n')
            self.threshold_object = 0.5

    def run(self, img) -> List[DetectedObject]:
        # runs the model on the provided image
        """Runs the model on the provided image

        This method runs the model on the image. It then interprets and organizes the output
        by classifying detections and constructing new :class:`arm_localizer.detected_object.DetectedObject`'s
        for each detection.

        Args:
            None right now but will change in next version

        Returns:
            detections: the model detections. changed in next version

        """
        self._claw=None
        self._base=None
        self._object=None


        img_tens = F.to_tensor(img)
        self._output = utils.load_model()([img_tens])
        boxes = self._output[0]['boxes']
        labels = self._output[0]['labels']
        masks = self._output[0]['masks']
        scores = self._output[0]['scores']
        self._detections = []
        for i in range(len(boxes)):
            label, box, mask, score = labels[i],boxes[i], masks[i], scores[i]
            label_string = utils.get_label_string(label)
            obj = DetectedObject(label_string, box, mask, score)
            if(label_string == utils.CLAW_STRING):
                obj.set_threshold(self.threshold_claw)
                if self._claw==None:
                  self._claw=obj
                elif score >self._claw.score:
                  self._claw=obj
            if(label_string == utils.BASE_STRING):
                obj.set_threshold(self.threshold_base)
                if self._base==None:
                  self._base=obj
                elif score >self._base.score:
                  self._base=obj
            if(label_string == utils.OBJECT_STRING):
                obj.set_threshold(self.threshold_object)
                if self._object==None:
                  self._object=obj
                elif score >self._object.score:
                  self._object=obj

        self._detections.append(self._claw)
        self._detections.append(self._base)
        self._detections.append(self._object)

        return self._detections

    def get_model_outputs(self):
        """Gets the raw output from the model

        Returns a tensor which includes the raw output from the model. mask, score, label, and box data for each detection

        Args:
           none

        Returns:
            tensor: A tensor that includes all of the outputs from the model

        """
        return self._output

    def get_all_detections(self):
        """Returns a list of DetectedObjects from the model outputs

        This function returns all of the detections from the model in the form of DetectedObjects, as a list

        Args:
            none

        Returns:
            List of DetectedObjects: all of the detections from the model as DetectedObjects

        """
        return self._detections
    
    def get_claw(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        for obj in self._detections:
            if obj.get_label() == utils.CLAW_STRING:
                return obj
        return False #consider alternative returns?
        
    def get_base(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        for obj in self._detections:
            if obj.get_label() == utils.BASE_STRING:
                return obj
        return False #consider alternative returns?

    def get_object(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        for obj in self._detections:
            if obj.get_label() == utils.OBJECT_STRING:
                return obj
        return False #consider alternative returns?
    

class LocalizerNotInitializedError(Exception):
    pass

class Localizer:
    
    def __init__(self):
        filename = "./rotation/rotation.pkl"
        try:
            fh = open(filename, "rb")
            fh_new = pickle.load(fh)
            self.rotation = fh_new
            fh.close()
        except Exception as e:
            print(e)
            raise LocalizerNotInitializedError(f"Unable to load rotation. Need to load rotation to initialize package {filename}.")
        
    def get_real_position(self, t_vector: Vector) -> Vector:
        """Applies the relevant saved transformation to the vector that is passed. Returns the converted position vector.

        This function applies the two saved rotations, in order, to convert the a vector between coordinate systems.

        Args:
            t_vector (Vector): The position (as a vector), relative to the camera system.
            

        Returns:
            Vector: The converted position vector

        """
        t_vector=t_vector.rotate_about_vector(self.rotation._f_rot_vector, self.rotation._f_rot_rads)
        t_vector=t_vector.rotate_about_vector(self.rotation._s_rot_vector, self.rotation._s_rot_rads)
        return t_vector
    

# def calibrate(img1: Image, depth1: np.ndarray, img2: Image, depth2: np.ndarray, pos_claw_1, pos_claw_2):
#     """This function calculates and saves the relevant transformation information for converting positions between the camera coordinate system and the robot arm coordinate system

#     This function accepts two images and two depth arrays, each pair of which corresponds with a different claw position
#     The function is also passed the actual claw positions as gotten from the positioning system of the robot arm.
#     This function then uses the ObjectDetector to detect and calculate the position of the claw from the camera's perspective.
#     Then, we use the actual claw positions to generate relevant transformations to align the coordinate systems.
#     This is then saved and will be used to convert any other positions to the robot arm coordinate system.

#     Args:
#         img1 (Image): The first image, rgb data
#         depth1 (np.ndarray): The first depth array, depths in mm
#         img2 (Image): The second image
#         depth2 (np.ndarray): The second depth array
#         pos_claw_1(Vector): The position of the claw from the Robot arm coordinate system which corresponds to the first depth and img
#         pos_claw_2(Vector): The position of the claw from the Robot arm coordinate system which corresponds to the second depth and img

#     Returns:
#         none

#     """
#     detector = ObjectDetector()

#     detector.run(img1)
#     cam_to_claw_1 = detector.get_claw().to_vector(img1.size, depth1)
#     cam_to_base_1 = detector.get_base().to_vector(img1.size, depth1)
#     base_to_claw_1 = cam_to_claw_1 - cam_to_base_1
    
#     detector.run(img2)
#     cam_to_claw_2 = detector.get_claw().to_vector(img2.size, depth2)
#     cam_to_base_2 = detector.get_base().to_vector(img2.size, depth2)
#     base_to_claw_2 = cam_to_claw_2 - cam_to_base_2
    
#     first_rot_vector = base_to_claw_1.cross(pos_claw_1)
#     first_rot_rads = base_to_claw_1.angle_between(pos_claw_1)
    
#     second_rot_vector = pos_claw_1

#     base_to_claw_2 = base_to_claw_2.rotate_about_vector(first_rot_vector.unit(), first_rot_rads)
#     pc2_perp = pos_claw_2.perp(second_rot_vector)
#     bc2_perp = base_to_claw_2.perp(second_rot_vector)
#     second_rot_rads = base_to_claw_2.perp(second_rot_vector).angle_between(pc2_perp)
#     if bc2_perp.cross(pc2_perp).dot(second_rot_vector.unit()) < 0:
#         second_rot_rads = -1 * second_rot_rads
    
#     rotation = Rotation(first_rot_vector, first_rot_rads, second_rot_vector, second_rot_rads)
    
#     utils.pickle_obj(rotation)

def rs_calibrate(img1: Image, depth1: np.ndarray, img2: Image, depth2: np.ndarray, pos_claw_1, pos_claw_2, 
        object_detector = None, threshold_claw = 0.5, threshold_base = 0.5, threshold_object = 0.5):
    """This function calculates and saves the relevant transformation information for converting positions between the camera coordinate system and the robot arm coordinate system

    This function accepts two images and two depth arrays, each pair of which corresponds with a different claw position
    The function is also passed the actual claw positions as gotten from the positioning system of the robot arm.
    This function then uses the ObjectDetector to detect and calculate the position of the claw from the camera's perspective.
    Then, we use the actual claw positions to generate relevant transformations to align the coordinate systems.
    This is then saved and will be used to convert any other positions to the robot arm coordinate system.
    This function uses the pyrealsense deproject pixel to calculate the position vectors


    Args:
        img1 (Image): The first image, rgb data
        depth1 (np.ndarray): The first depth array, depths in mm
        img2 (Image): The second image
        depth2 (np.ndarray): The second depth array
        pos_claw_1(Vector): The position of the claw from the Robot arm coordinate system which corresponds to the first depth and img
        pos_claw_2(Vector): The position of the claw from the Robot arm coordinate system which corresponds to the second depth and img

    Returns:
        none

    """
    if (object_detector == None):
        detector = ObjectDetector(threshold_claw, threshold_base, threshold_object)
    else:
        detector = object_detector

    detector.run(img1)
    cam_to_claw_1 = detector.get_claw().rs_to_vector(depth1)
    cam_to_base_1 = detector.get_base().rs_to_vector(depth1)
    base_to_claw_1 = cam_to_claw_1 - cam_to_base_1
    
    detector.run(img2)
    cam_to_claw_2 = detector.get_claw().rs_to_vector(depth2)
    cam_to_base_2 = detector.get_base().rs_to_vector(depth2)
    base_to_claw_2 = cam_to_claw_2 - cam_to_base_2
    
    first_rot_vector = base_to_claw_1.cross(pos_claw_1)
    first_rot_rads = base_to_claw_1.angle_between(pos_claw_1)
    
    second_rot_vector = pos_claw_1

    base_to_claw_2 = base_to_claw_2.rotate_about_vector(first_rot_vector.unit(), first_rot_rads)
    pc2_perp = pos_claw_2.perp(second_rot_vector)
    bc2_perp = base_to_claw_2.perp(second_rot_vector)
    second_rot_rads = base_to_claw_2.perp(second_rot_vector).angle_between(pc2_perp)
    if bc2_perp.cross(pc2_perp).dot(second_rot_vector.unit()) < 0:
        second_rot_rads = -1 * second_rot_rads
    
    rotation = Rotation(first_rot_vector, first_rot_rads, second_rot_vector, second_rot_rads)
    
    utils.pickle_obj(rotation)

def get_object_position(img, depth, object_detector = None, threshold_claw = 0.5, threshold_base = 0.5, threshold_object = 0.5):
    """This function calculates the position of the detected object in the image, relative to the robot arm's positioning system

    This function first runs the model on the image, then it gets the vector for the claw detection relative to the camera.
    then it converts that position to be relative to the robot arm's coordinate system.

    Args:
        img (Image): The image with the object to be located
        depth (np.ndarray): The depth array corresponding to the image

    Returns:
        Vector: The position of the object, relative to the coordinate system of the Robot arm, in millimeters

    """
    l = Localizer()

    if (object_detector == None):
        d = ObjectDetector(threshold_claw, threshold_base, threshold_object)
    else:
        d = object_detector

    d.run(img)
    target = d.get_object().rs_to_vector(depth) - d.get_base().rs_to_vector(depth)
    real_pos = l.get_real_position(target)
    return real_pos