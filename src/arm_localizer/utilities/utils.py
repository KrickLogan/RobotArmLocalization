from fileinput import filename
import torch
from PIL import Image
import os
import numpy as np
import numpy.ma as ma
from math import tan
import pickle as pickle
from arm_localizer import ObjectDetector, Vector, Rotation
# from arm_localizer.vector import Vector

# from arm_localizer.rotation import Rotation

PRECISION = 0.6
BASE_STRING = 'Base'
CLAW_STRING = 'Claw'
COTTON_STRING = 'Cotton'
BACKGROUND_STRING = 'Background'
ERROR_STRING = 'ERROR'
HFOV = 69 #degrees
VFOV = 42 #degrees

def load_model():
    # dirname = os.path.join(os.path.dirname(__file__),"../camera_data/depths/")
    model = torch.load(os.path.join(os.path.dirname(__file__),'../data/model/model.pt'), map_location=torch.device('cpu'))
    return model

def load_image(img_file_name):
    dirname = "./camera_data/images/"
    img = Image.open(os.path.join(dirname,img_file_name)).convert("RGB")
    return img

def load_depth_arr(dp_arr_name):
    # dirname = os.path.join(os.path.dirname(__file__),"../camera_data/depths/")
    # dirname.replace(r'\\','/')
    dirname = "./camera_data/depths/"
    np_depth = np.load(os.path.join(dirname, dp_arr_name))
    return np_depth

# def get_center_point(box):
#     x1, y1, x2, y2 = box.detach().numpy()
#     x = (x1 + x2)/2
#     y = (y1 + y2)/2
#     return((x,y))

# def get_bool_mask(mask):   
#     bool_mask = mask > PRECISION 
#     assert bool_mask.ndim == 2
#     bool_mask = bool_mask.squeeze(1) #########Maybeeee???
#     return bool_mask

# def get_avg_depth(bool_mask, depth_arr):
#     bool_mask = np.logical_and(bool_mask, depth_arr != 0)
#     bool_mask = torch.gt(bool_mask, 0)
#     mx = ma.masked_array(depth_arr, np.invert(bool_mask).long())
#     return mx.mean()

def get_vfov():
    return VFOV

def get_hfov():
    return HFOV

# def calculate_vector(box_center_pxl, img_center_pxl, depth):
#     vertical_fov = get_vfov()
#     horiz_fov = get_hfov()
#     # z_angle = get_angle_between_pxls(box_center_pxl[1], img_center_pxl[1], vertical_fov) #angle in zy plane-angle of elevation
#     # x_angle = get_angle_between_pxls(box_center_pxl[0], img_center_pxl[0], horiz_fov) #Angle in xy plane
#     x_angle, z_angle = get_angles_between_pixels(box_center_pxl, img_center_pxl, vertical_fov, horiz_fov)
#     z = get_coord_value(z_angle, depth)
#     x = get_coord_value(x_angle, depth)
#     y = depth
#     return (x,y,z)

def get_label_string(label): ## Rework to use a dict?
    label_string = ''
    if label == 1:
        label_string = BASE_STRING
    elif label == 2:
        label_string = CLAW_STRING
    elif label == 3:
        label_string = COTTON_STRING
    elif label == 0:
        label_string = BACKGROUND_STRING
    else:
        label_string = ERROR_STRING
    return label_string

# def get_angle_between_pxls(box_val, img_val, fov): ## there will be an issue with the axis. y pixel value goes top to bottom 0-height
#     return (box_val-img_val)*(fov/2)/img_val

# def get_angles_between_pixels(box_center_pxl, img_center_pxl, vertical_fov, horiz_fov):
#     box_x, box_z = box_center_pxl
#     img_x, img_z = img_center_pxl
#     x_angle = (box_x - img_x)*(horiz_fov/2)/(img_x)
#     z_angle = (box_z - img_z)*(vertical_fov/2)/(img_z)
#     return x_angle, z_angle

# def get_coord_value(angle, depth):
#     return depth * tan(angle)

def fail(frameinfo):
    print(frameinfo.filename, frameinfo.lineno)
    #Should start throwing exceptions instead of this wherever this function is called

# def calibrate(cam_claw_1: Vector, pos_claw_1: Vector, cam_claw_2: Vector, pos_claw_2: Vector):
#     f_rot_vector = cam_claw_1.cross(pos_claw_1)
#     f_rot_rads = cam_claw_1.angle_between(pos_claw_1)
#     s_rot_vector = pos_claw_1
#     cam_claw_2 = cam_claw_2.rotate_about_vector(f_rot_vector.unit(), f_rot_rads)
#     s_rot_rads = cam_claw_2.perp(s_rot_vector).angle_between(pos_claw_2.perp(s_rot_vector))
#     rotation = Rotation(f_rot_vector, f_rot_rads, s_rot_vector, s_rot_rads)
#     pickle_obj(rotation)

def get_img_size(img):
    return img.size

def calibrate(img1: Image, depth1: np.ndarray, img2: Image, depth2: np.ndarray, pos_claw_1, pos_claw_2):
    
    detector = ObjectDetector()

    detector.run(img1)
    cam_to_claw_1 = detector.get_claw().to_vector(get_img_size(img1), depth1)
    cam_to_base_1 = detector.get_base().to_vector(get_img_size(img1), depth1)
    base_to_claw_1 = cam_to_claw_1 - cam_to_base_1
    
    detector.run(img2)
    cam_to_claw_2 = detector.get_claw().to_vector(get_img_size(img2), depth2)
    cam_to_base_2 = detector.get_base().to_vector(get_img_size(img2), depth2)
    base_to_claw_2 = cam_to_claw_2 - cam_to_base_2
    
    first_rot_vector = base_to_claw_1.cross(pos_claw_1)
    first_rot_rads = base_to_claw_1.angle_between(pos_claw_1)
    
    second_rot_vector = pos_claw_1

    base_to_claw_2 = base_to_claw_2.rotate_about_vector(first_rot_vector.unit(), first_rot_rads)
    second_rot_rads = base_to_claw_2.perp(second_rot_vector).angle_between(pos_claw_2.perp(second_rot_vector))
    rotation = Rotation(first_rot_vector, first_rot_rads, second_rot_vector, second_rot_rads)
    
    pickle_obj(rotation)


def pickle_obj(obj):#, filename): #new pickling function, should be able to pickle any object.
    filename = "./rotation/rotation.pickle"
    fh = open(filename, "bw")
    pickle.dump(obj, fh)
    fh.close()

def unpickle():#, filename): #new unpickling function, should be able to unpickle any object.
    # dirname = "./rotation/"
    filename = "./rotation/rotation.pickle"
    fh = open(filename, "rb")
    try:
        fh_new = pickle.load(fh)
    except pickle.UnpicklingError as e:
        print(e)
    fh.close()
    return fh_new