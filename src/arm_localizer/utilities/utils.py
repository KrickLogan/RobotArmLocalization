import torch
from PIL import Image
import os
import numpy as np
import pickle as pickle

BASE_STRING = 'Base'
CLAW_STRING = 'Claw'
OBJECT_STRING = 'Object'
BACKGROUND_STRING = 'Background'
ERROR_STRING = 'ERROR'
# HFOV and VFOV are no longer used and part of the old system that doesn't use pyrealsense2
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
    """HFOV and VFOV are no longer used and part of the old system that doesn't use pyrealsense2.
    Gets the Vertical Field of Vision of the camera in degrees
    """
    return VFOV

def get_hfov():
    """HFOV and VFOV are no longer used and part of the old system that doesn't use pyrealsense2.
    Gets the Horizontal Field of Vision of the camera in degrees
    """
    return HFOV

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
        label_string = OBJECT_STRING
    elif label == 0:
        label_string = BACKGROUND_STRING
    else:
        label_string = ERROR_STRING
    return label_string

def pickle_obj(obj):#, filename): #new pickling function, should be able to pickle any object.
    create_rotation_folder()
    filename = "./rotation/rotation.pkl"
    fh = open(filename, "bw")
    pickle.dump(obj, fh)
    fh.close()

def create_rotation_folder():    
    newdir = "./rotation"
    if not os.path.exists(newdir):
        os.makedirs(newdir)
