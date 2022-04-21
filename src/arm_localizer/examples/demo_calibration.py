import matplotlib.pyplot as plt
from arm_localizer import *
from arm_localizer import visualizer as viz
from math import radians, degrees
from PIL import Image
import os    


# This File demonstrates how to calibrate the system for repeated usage. Using the 
# images, depth arrays, and known claw positions, a rotation object will be saved and
# referenced from the users working directory. It is critical that this rotation is present
# for continued usage of the system.
# Run this file before trying to get the position of the object in the images.

def main():
    
    # Put your path to the first image here
    img1_filename = "./camera_data/images/3_15_22/position_1/claw_1.png"
    # Put your path to the second image here
    img2_filename = "./camera_data/images/3_15_22/position_1/claw_2.png"

    # Put your path to the first depth here 
    depth1_filename = "./camera_data/depths/3_15_22/position_1/claw_1_depth.npy"
    # Put your path to the second depth here
    depth2_filename = "./camera_data/depths/3_15_22/position_1/claw_2_depth.npy"

    # Load the first image and open as an RGB image, load the first depth array (measured in mm)
    img1 = Image.open(os.path.join(img1_filename)).convert("RGB") 
    depth_arr1 = np.load(os.path.join(depth1_filename))  

    # Put in the measure position of the claw from the robot arm or get the postition of the claw from the robot arm
    pos_claw_1 = Vector(247, 110, 211) 

    # Load the second image and open as an RGB image, load the second depth array (measured in mm). 
    img2 = Image.open(os.path.join(img2_filename)).convert("RGB")    
    depth_arr2 = np.load(os.path.join(depth2_filename))

    # Put in the measure position of the claw from the robot arm or get the postition of the claw from the robot arm
    pos_claw_2 = Vector(268, -90, 173)

    # calculates a transformation for converting positions between the camera coordinate system and the robot arm system. 
    # Important: Needs to have both sets of images, depths and claws to complete this rotation.
    # The end result is a new rotation folder and file saved
    rs_calibrate(img1, depth_arr1, img2, depth_arr2, pos_claw_1, pos_claw_2)    
    
if __name__ == "__main__":
    main()
