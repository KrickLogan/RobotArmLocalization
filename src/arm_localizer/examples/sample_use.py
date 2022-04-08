import arm_localizer
from PIL import Image
import numpy as np


def calibrate():

    #Each time the camera system is setup in a certain position, this calibration must be run
    # if the camera does not move, you can continuously run detections and get positions
    # The calibration must be re rean if the camera moves

    #The positions of the claws relative to the coordinate system you are transforming TO
    pos_claw_1 = arm_localizer.Vector(247, 110, 211)
    pos_claw_2 = arm_localizer.Vector(268, -90, 173)

    # Images corresponding to the two claw positions
    img1 = Image.open("/path/to/img1")
    dp1 = np.load("/path/to/depth1")
    img2 = Image.open("/path/to/img1")
    dp2 = np.load("/path/to/depth1")

    #rs_calibrate will create and save a rotation object in htis directory which will be accessed when running
    # the localizer when arm_localizer.get_obj_position is called

    arm_localizer.rs_calibrate(img1, dp1, img2, dp2, pos_claw_1, pos_claw_2)


def get_position():

    img = Image.open("/path/to/img1")
    dp = np.load("/path/to/depth1")

    #This call runs the model on the image and calculates the object's position and applies the rotation from the calibration step
    # Above. Gives the 3d position of the object, relative to the base, in millimeters

    obj_position = arm_localizer.get_object_position(img, dp)

    print(obj_position)

