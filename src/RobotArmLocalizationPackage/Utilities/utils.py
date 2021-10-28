import torch
from PIL import Image
import os
import numpy as np
import pytest
import numpy.ma as ma

PRECISION = 0.75
BASE_STRING = 'Base'
CLAW_STRING = 'Claw'
COTTON_STRING = 'Cotton'
BACKGROUND_STRING = 'Background'
ERROR_STRING = 'ERROR'

def load_model():
    model = torch.load('model.pt', map_location=torch.device('cpu'))
    return model

def load_image(img_file_name):
    img = Image.open(os.path.join("Data/Images/",img_file_name)).convert("RGB")

def load_depth_arr(dp_arr_name):
    np_depth = np.load(os.path.join("Data/Depths/", dp_arr_name))
    return np_depth

def get_center_point(mask):
    return (0,0) #To be filled w/ jacobs fn

def get_bool_mask(mask):   
    bool_mask = mask > PRECISION 
    assert bool_mask.ndim == 2
    bool_mask = bool_mask.squeeze(1) #########Maybeeee???
    return bool_mask

def get_avg_depth(bool_mask, depth_arr):
    bool_mask = np.logical_and(bool_mask, depth_arr != 0)
    bool_mask = torch.gt(bool_mask, 0)
    mx = ma.masked_array(depth_arr, np.invert(bool_mask).long())
    return mx.mean()

def calculate_vector(box_center_pxl, img_center_pxl, depth, HFOV, VFOV):
    z_angle = get_angle_between_pxls(box_center_pxl[1], img_center_pxl[1], VFOV) #angle in zy plane
    x_angle = get_angle_between_pxls(box_center_pxl[0], img_center_pxl[0], HFOV) #Angle in xy plane
    z = get_coord_value(z_angle, depth)
    x = get_coord_value(x_angle, depth)
    y = depth
    return (x,y,z)

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

def get_angle_between_pxls(px1, px2, FOV):
    #SomethingHere
    # return angle

def get_coord_value(angle, depth):
    #Something Here
    #return coordinate value