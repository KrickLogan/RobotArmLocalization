import torch
from PIL import Image
import os
import numpy as np
import pickle as pickle
import pyrealsense2 as rs

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

def pickle_obj(obj):
    create_rotation_folder()
    fh = open("./rotation/rotation.pkl", "bw")
    pickle.dump(obj, fh)
    fh.close()

def create_rotation_folder():    
    newdir = "./rotation"
    if not os.path.exists(newdir):
        os.makedirs(newdir)

def _get_intrinsics_from_stream(cfg):
    depth_profile = cfg.get_stream(rs.stream.depth) # Fetch stream profile for depth stream
    depth_intr = depth_profile.as_video_stream_profile().get_intrinsics() # Downcast to video_stream_profile and fetch intrinsics
    color_profile = cfg.get_stream(rs.stream.color)
    color_intr = color_profile.as_video_stream_profile().get_intrinsics()
    print("color intrinsics:\n", color_intr,"\n\nDepth Intr: \n", depth_intr)
    return color_intr, depth_intr

def get_intrinsics():
    '''This function is to be used if yu have a real sense camera currently hooked up to your device

    This function will save the color intrinsics information for the camera and will use that data
    when calculating vectors in the object detector
    
    '''
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()

    depth_sensor = device.first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    device_product_line = str(device.get_info(rs.camera_info.product_line))

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30) # was 640 x 480 instead of 1920 x 1080 1280, 720, 640, 480

    if device_product_line == 'L500':
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # was 640 x 480 instead of 1920 x 1080
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # was 640 x 480 instead of 1920 x 1080

    cfg = pipeline.start(config)

    color_intr, depth_intr = _get_intrinsics_from_stream(cfg)

    # print(depth_intr.width, depth_intr.height, depth_intr.fx, depth_intr.fy, depth_intr.ppy, depth_intr.ppx, depth_intr.model, depth_intr.coeffs)

    ci_dict = {
                'width': color_intr.width, 
                'height': color_intr.height, 
                'fx': color_intr.fx, 
                'fy': color_intr.fy, 
                'ppy': color_intr.ppy, 
                'ppx': color_intr.ppx, 
                'model': color_intr.model, 
                'coeffs': color_intr.coeffs
                }

    filename = 'color_intrinsics'
    new_dir = './intrinsics'
    if not os.path.exists(new_dir):
            os.makedirs(new_dir)
    outfile = open(os.path.join(new_dir, filename),'wb')

    pickle.dump(ci_dict,outfile)

    outfile.close()

    print("Intrinsics located in ./intrinsics/color_intrinsics")
