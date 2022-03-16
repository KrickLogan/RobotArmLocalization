# This file demonstrates all the features of the system as it
#  stands on 12/6/2021

from arm_localizer.object_detector import ObjectDetector
from arm_localizer.detected_object import DetectedObject
from arm_localizer.localizer import Localizer
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz
import matplotlib.pyplot as plt
from PIL import ImageOps

def main():
    frame_prefix = "frame_20"
    img = utils.load_image(frame_prefix + ".png")
    plt.imshow(img)
    plt.show()
    # img = ImageOps.mirror(img) # i had a dream where I needed to check if the mirrors worked. it does but does not recognize claw upside down.
    # plt.imshow(img)
    # plt.show()
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")

    detector = ObjectDetector(img) # provide image to model
    
    detector.run() # Run model on image

    # The following get the model outputs for each of the detections

    claw = detector.get_claw()
    base = detector.get_base()
    obj = detector.get_object()
    detections = [claw, base, obj]
    print("demonstrating getting the detections from the detector class:\n")
    for det in detections:
        print(f"Label: {det.label} Score: {det.score}")
        input()
    
    # Use the visualizer to show the boxes and the center points

    rectangles = viz.get_rectangles([claw.box, base.box, obj.box])
    viz.show_img_boxes(img, rectangles)
    claw_center = claw.get_center_pixel()
    viz.show_point(img, claw_center, f"Center Point Coordinates: {claw_center}")
    base_center = base.get_center_pixel()
    viz.show_point(img, base_center, f"Center Point Coordinates: {base_center}")
    obj_center = obj.get_center_pixel()
    viz.show_point(img, obj_center, f"Center Point Coordinates: {obj_center}")

    # Mask calculations are done by using a boolean array, called bool mask, with
    #  index values correlating to pixels and whether it contains the object or not

    bmask = claw.get_bool_mask()

    viz.show_mask_overlay(img=depth_arr, mask=bmask, title="Depth Values of claw", depth_arr=depth_arr, force_contrast=True)

    claw_depth = claw.get_average_depth(depth_arr)
    base_depth = base.get_average_depth(depth_arr)
    obj_depth = obj.get_average_depth(depth_arr)

    print(f"Claw Depth: {claw_depth}")
    input()
    print(f"Base Depth: {base_depth}")
    input()
    print(f"Object Depth: {obj_depth}")
    input()

    localizer = Localizer(detector, depth_arr)
    norm_claw_center = localizer.normalize_pixel_value(claw_center, [img.size[0]/2, img.size[1]/2])
    norm_base_center = localizer.normalize_pixel_value(base_center, [img.size[0]/2, img.size[1]/2])
    norm_obj_center = localizer.normalize_pixel_value(obj_center, [img.size[0]/2, img.size[1]/2])
    
    print("Claw Normalized Pixel Coordinates: ", norm_claw_center)
    input()
    print("Base Normalized Pixel Coordinates: ", norm_base_center)
    input()
    print("Object Normalized Pixel Coordinates: ", norm_obj_center)
    input()

    print("Vectors of Objects relative to Camera:\n")
    print("Claw Vector: ", localizer.claw_vector)
    print("Base Vector: ", localizer.base_vector)
    print("Object Vector: ", localizer.object_vector)
    
    # print("Preliminary rotation adjustment: ")
    # localizer.

    print("Target Vector: ", localizer.target_vector)



if __name__ == "__main__":
    main()
