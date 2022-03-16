import torch
from PIL import Image
import os
import numpy as np
import numpy.ma as ma
from math import tan
import pickle as pickle
# from arm_localizer import ObjectDetector, Vector, Rotation
# from arm_localizer.vector import Vector

# from arm_localizer.rotation import Rotation

PRECISION = 0.5
BASE_STRING = 'Base'
CLAW_STRING = 'Claw'
COTTON_STRING = 'Cotton'
BACKGROUND_STRING = 'Background'
ERROR_STRING = 'ERROR'
HFOV = 69 #degrees
VFOV = 42 #degrees
def load_model():

    model = torch.load(os.path.join(os.path.dirname(__file__),'../data/model/model.pt'), map_location=torch.device('cpu'))
    return model

def load_image(img_file_name):
    dirname = "./camera_data/images/"
    img = Image.open(os.path.join(dirname,img_file_name)).convert("RGB")
    return img

def load_depth_arr(dp_arr_name):

    dirname = "./camera_data/depths/"
    np_depth = np.load(os.path.join(dirname, dp_arr_name))
    return np_depth

def get_vfov():
    """Gets the Vertical Field of Vision of the camera in degrees
    """
    return VFOV

def get_hfov():
    """Gets the Horizontal Field of Vision of the camera in degrees
    """
    return HFOV

def Set_vfov(new_vfov):
    """Sets the Vertical Field of Vision of the camera in degrees
    """
    return VFOV

def set_hfov(new_hfov):
    """Sets the Horizontal Field of Vision of the camera in degrees
    """
    HFOV = new_hfov

def get_label_string(label): ## Rework to use a dict?
    """Converts the integer label from the model to a human readable string

        TODO should probably go into detected object
    """
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

def create_rotation_folder():    
    newdir = "./rotation"
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    else:
        print("folder already exists")