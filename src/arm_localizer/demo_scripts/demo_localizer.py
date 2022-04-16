from arm_localizer import *
from arm_localizer import visualizer as viz
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from math import degrees

def main(): 

    # Put your path to the image here
    img_filename = "./camera_data/images/3_15_22/position_1/claw_1.png"    

    # Put your path to the depth here
    depth_filename = "./camera_data/depths/3_15_22/position_1/claw_1_depth.npy"

    # Load the first image and open as an RGB image, load the first depth array (measured in mm) 
    img = Image.open(os.path.join(img_filename)).convert("RGB") 

    depth_arr = np.load(os.path.join(depth_filename)) 
    
    # initiates detector as the pointer to the detections (output) from the model
    detector = ObjectDetector()

    # run the second image on the ObjectDetector to get the detections from the model
    detector.run(img)

    # Initializes the obj_vector that stores the detected objects converted position vector
    obj_vector = detector.get_object().rs_to_vector(depth_arr) - detector.get_base().rs_to_vector(depth_arr)
   
    # initialize l to point to the localizer function
    l = Localizer()

    # stores the true position of the detected object after conversion. You need to have both saved rotations from the demo_calibration in 
    # order for get_real_position to return the true position after calculation. The localizer calls this function to get the result that we want.
    calculated_position = l.get_real_position(obj_vector)  
    print (f"calculated position: {calculated_position}")    

if __name__ == "__main__":
    main()
