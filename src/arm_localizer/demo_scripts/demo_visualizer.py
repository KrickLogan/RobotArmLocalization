from arm_localizer import ObjectDetector
from arm_localizer.demo_scripts.demo_calibration import get_center_points
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz

def main():
    frame_prefix = "frame_0"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")

    viz.show_img(img)
    
    detector = ObjectDetector() # provide image to model

    detector.run(img) # Run model on image

    # The following get the model outputs for each of the detections

    claw = detector.get_claw()
    base = detector.get_base()
    obj = detector.get_object()

    # These are used to help showcase all the visualizer functions

    claw_center = claw.get_center_pixel()
    center_points = get_center_points(detector)

    # One detection overlaid with its depth
    print("This function showcases one set of img, mask, & depth overlaid on top of each other. In this case, the claw.\n")
    viz.show_mask_overlay(img, claw.get_bool_mask(), claw.get_label(), True, depth_arr)

    # All detection-masks overlaid with their imgs
    print("This function showcases the img with all three of its masks overlaid on top of it in separate instances.\n")
    viz.show_all_masks(img, detector.get_all_detections(), depth_arr)

    # One detection-mask overlaid with its img
    print("This function showcases the img and one mask overlaid together.")
    viz.show_mask(img, claw, depth_arr)

    # The center of the claw
    print("This function can be used to show any specific xy coordinate. In this case, it's used to show the center of the claw.\n")
    viz.show_point(img, claw_center, "Show Point")

    # The center of the base, claw, and obj
    print("This function can be used to showcase an entire set of specific xy coordinates. In this case, it shows all 3 center points for our detections.\n")
    viz.show_points(img, center_points, "Show Points/Center")

    # The center of the obj in a different function, not requiring line 31
    print("This function showcases the center point of a singular object, in this case, the cotton.\n")
    viz.show_center_point(img, obj, "Object/Center")

    # All bounding boxes for our detections
    print("This function showcases the bounding boxes surrounding all 3 detected objects in our img.\n")
    viz.show_img_boxes(img, detector.get_all_detections())


    # Bar graph with and without outliers
    print("This function has showcases a comparison bargraph showing the depth our detections are located at.")
    viz.show_depth_distribution(claw, depth_arr)

if __name__ == "__main__":
    main()
