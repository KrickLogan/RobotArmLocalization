import arm_localizer
from PIL import Image
import os
import numpy as np

def main(): 

    # Put your path to the image here
    img_filename = "./camera_data/images/3_15_22/position_1/claw_1.png"    

    # Put your path to the depth here
    depth_filename = "./camera_data/depths/3_15_22/position_1/claw_1_depth.npy"

    # Load the first image and open as an RGB image, load the first depth array (measured in mm) 
    img = Image.open(os.path.join(img_filename)).convert("RGB") 

    depth_arr = np.load(os.path.join(depth_filename))    
    
    # This function calculates the true position of the detected object after conversion. You need to have both saved rotations from the demo_calibration in 
    # order for get_object_position to return the true position after calculation. The localizer calls this function to get the result that we want.
    calculated_position = arm_localizer.get_object_position(img, depth_arr)  
    print (f"calculated position: {calculated_position}")    

if __name__ == "__main__":
    main()
