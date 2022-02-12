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

    detector = ObjectDetector(img1) # provide image to model
    
    detector.run() # Run model on image

    cam_claw_1 = detector.get_claw().to_vector(img1.size,depth_arr) - detector.get_base().to_vector(img1.size,depth_arr)
    pos_claw_1 = get_pos(cam_claw_1)

    img2 = get_image('frame_25')
    depth_arr2 = utils.load_depth_arr("frame_25_depth.npy")

    detector = ObjectDetector(img2) # provide image to model
    
    detector.run() # Run model on image

    cam_claw_2 = detector.get_claw().to_vector(img2.size,depth_arr2) - detector.get_base().to_vector(img2.size,depth_arr2)
    pos_claw_2 = get_pos(cam_claw_2)

    l = Localizer()
    l.calibrate(cam_claw_1, pos_claw_1, cam_claw_2, pos_claw_2)

    #Now we are ready to use the system.

    target = detector.get_object().to_vector(img2.size,depth_arr2) - detector.get_base().to_vector(img2.size,depth_arr2)

    calc_pos_vector = l.get_real_position(target)
    print(calc_pos_vector)


if __name__ == "__main__":
    main()
