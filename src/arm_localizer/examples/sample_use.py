import arm_localizer
from PIL import Image
import numpy as np


def calibrate():

    #Each time the camera system is setup in a certain position, this calibration must be run
    # if the camera does not move, you can continuously run detections and get positions
    # The calibration must be *run again* if the camera moves

    #The positions of the claws relative to the coordinate system you are transforming TO
    pos_claw_1 = arm_localizer.Vector(247, 110, 211)
    pos_claw_2 = arm_localizer.Vector(268, -90, 173)

    # Images corresponding to the two claw positions. you can change between the camera positions by
    # changing the folder to position_2 etc.

    img1 = Image.open("/path/to/img1") # /camera_data/position_1/images/claw_1.png
    dp1 = np.load("/path/to/depth1") # /camera_data/position_1/depths/claw_1.npy
    img2 = Image.open("/path/to/img1") # /camera_data/position_1/images/claw_2.png
    dp2 = np.load("/path/to/depth1") # /camera_data/position_1/depths/claw_2.npy

    #rs_calibrate will create and save a rotation object in htis directory which will be accessed when running
    # the localizer when arm_localizer.get_obj_position is called

    arm_localizer.rs_calibrate(img1, dp1, img2, dp2, pos_claw_1, pos_claw_2)

    

def get_position():

    img = Image.open("/path/to/img1") # /camera_data/position_1/images/obj_2.png *note there is no obj_1 image because that is in the claw_1 and claw_2 images
    dp = np.load("/path/to/depth1") # /camera_data/position_1/depths/obj_2.npy

    #This call runs the model on the image and calculates the object's position and applies the rotation from the calibration step
    # Above. Gives the 3d position of the object, relative to the base, in millimeters

    obj_position = arm_localizer.get_object_position(img, dp)

    print(obj_position)

    #Here are the correpsonding true positions, in millimeters, of each of the object positions:

    # object position 1 (439, -202, -22) corresponding image: claw_1 or claw_2.png
    # object position 2 (245, 202, -22) corresponding image: obj_2.png
    # object position 3 (459, 78, 205) corresponding image: obj_3.png
