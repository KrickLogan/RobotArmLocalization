from arm_localizer.object_detector import ObjectDetector
from arm_localizer.detected_object import DetectedObject
from arm_localizer.localizer import Localizer
import matplotlib.pyplot as plt
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz
from arm_localizer.vector import Vector
from math import radians, degrees


print(3)

# def get_pos():
    ##
def apply_rotation(v:Vector):
    x = 10
    y = -4
    z = 100
    v = v.rotate_about_vector(Vector(1,0,0),radians(x))
    v = v.rotate_about_vector(Vector(0,1,0),radians(y))
    v = v.rotate_about_vector(Vector(0,0,1),radians(z))
    return v

def get_pos(v:Vector):
    # This is a bad simulation of actually getting the arm position from the other system

    return apply_rotation(v)


def get_image(frame_prefix):
    img = utils.load_image(frame_prefix + ".png")
    plt.imshow(img)
    plt.show()
    return img

def main():
    # frame_prefix = "arm_localizer/"
    img1 = get_image('frame_20')
    
    depth_arr = utils.load_depth_arr("frame_20_depth.npy")
    print("calibration routine procedure:")
    print("run detection on first image")
    detector = ObjectDetector(img1) # provide image to model
    
    detector.run() # Run model on image
    viz.show_mask_overlay(img1, detector.get_claw().get_bool_mask(), "claw detection")
    print("get relevant claw vectors")
    cam_claw_1 = detector.get_claw().to_vector(img1.size,depth_arr) - detector.get_base().to_vector(img1.size,depth_arr)
    pos_claw_1 = get_pos(cam_claw_1)
    print(f"camera's perspective, claw vector: {cam_claw_1}")
    print(f"robot arm's perspective, claw vector: {pos_claw_1}")
    
    img2 = get_image('frame_112')
    depth_arr2 = utils.load_depth_arr("frame_112_depth.npy")

    detector = ObjectDetector(img2) # provide image to model
    
    detector.run() # Run model on image
    viz.show_mask_overlay(img2, detector.get_claw().get_bool_mask(), "claw detection")
    cam_claw_2 = detector.get_claw().to_vector(img2.size,depth_arr2) - detector.get_base().to_vector(img2.size,depth_arr2)
    pos_claw_2 = get_pos(cam_claw_2)
    print(f"camera's perspective, claw vector: {cam_claw_2}")
    print(f"robot arm's perspective, claw vector: {pos_claw_2}")
    
    
    utils.calibrate(cam_claw_1, pos_claw_1, cam_claw_2, pos_claw_2)
    print("save the rotation")
    l = Localizer()
    #Now we are ready to use the system.

    print("take a new image with target in it and get the target vector")
    img3 = get_image('frame_20')
    depth_arr3 = utils.load_depth_arr("frame_20_depth.npy")

    detector = ObjectDetector(img3) # provide image to model
    
    detector.run() # Run model on image
    viz.show_mask_overlay(img3, detector.get_object().get_bool_mask(), "claw detection")
    target = detector.get_object().to_vector(img3.size, depth_arr3) - detector.get_base().to_vector(img3.size, depth_arr3)
    print(f"now get object vector from system: {target}")
    print()
    calc_pos_vector = l.get_real_position(target)
    print(f"apply the rotation to the target vector to get the position relative to the robot arm")
    print()
    print(f"the calculated position vector: {calc_pos_vector}")
    input()
    print()
    print()
    
    print(f"Applying the same rotation in a test scenario, we show that this process does give the correct angle: {get_pos(target)}")

if __name__ == "__main__":
    main()
