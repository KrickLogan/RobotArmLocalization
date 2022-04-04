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
    viz.show_mask_overlay(img, claw.get_bool_mask(), claw.get_label(), True, depth_arr)

    # All detection-masks overlaid with their imgs
    viz.show_all_masks(img, detector.get_all_detections(), depth_arr)

    # One detection-mask overlaid with its img
    viz.show_mask(img, claw, depth_arr)

    # The center of the claw
    viz.show_point(img, claw_center, "Show Point")

    # The center of the base, claw, and obj
    viz.show_points(img, center_points, "Show Points/Center")

    # The center of the obj in a different function, not requiring line 31
    viz.show_center_point(img, obj, "Object/Center")

    # All bounding boxes for our detections
    viz.show_img_boxes(img, detector.get_all_detections())


    # Bar graph with and without outliers

    data_lables, data_values = viz.get_graph_labels_values(claw.get_masked_array(depth_arr))
    viz.show_bar_graph(data_lables,data_values,"With Outliers")
    no_outliers_arr = base.remove_depth_outliers(claw.get_masked_array(depth_arr))
    data_lables, data_values = viz.get_graph_labels_values(no_outliers_arr)
    viz.show_bar_graph(data_lables,data_values,"No Outliers")

if __name__ == "__main__":
    main()
