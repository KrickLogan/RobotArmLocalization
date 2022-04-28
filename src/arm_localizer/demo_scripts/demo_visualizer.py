from arm_localizer import ObjectDetector
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz

def main():
    frame_prefix = "frame_0"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")

    print("This just showcases the original image.\n")
    viz.show_img(img)
    
    detector = ObjectDetector() # provide image to model

    detector.run(img) # Run model on image

    # The following get the model outputs for each of the detections

    claw = detector.get_claw()
    base = detector.get_base()
    obj = detector.get_object()

    # One detection-mask overlaid with its img
    print("This function showcases the img and one mask overlaid together, in this case, the cotton.\n")
    viz.show_mask(obj, img, depth_arr)

    # All detection-masks overlaid with their imgs
    print("This function showcases the img with all three of its masks overlaid on top of it in separate instances.\n")
    viz.show_all_masks(detector.get_all_detections(), img, depth_arr)

    # Display the center point of an object
    print("This function showcases the center point of a singular object, in this case, the base.\n")
    viz.show_center_point(base, img, "Base Center Point")

    # Display the center point of all three objects
    print("This function showcases the center point of all three objects.\n")
    viz.show_center_points(detector.get_all_detections(), img, "All Center Points")

    # One bounding box for a detections
    print("This function showcases a bounding box around a singular object, in this case, the cotton.\n")
    viz.show_img_box(obj, img, "Cotton Bounding Box")

    # All bounding boxes for our detections
    print("This function showcases the bounding boxes surrounding all 3 detected objects in our img.\n")
    viz.show_img_boxes(detector.get_all_detections(), img, "All Bounding Boxes")

    # Bar graph with and without outliers
    print("This function has showcases a comparison bargraph showing the depth our detections are located at.")
    viz.show_depth_distribution(claw, depth_arr, "Outlier Detection")

if __name__ == "__main__":
    main()
