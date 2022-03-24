# This file is used for demonstrating the model
# as it stands on 2/20/2022

from arm_localizer.arm_localizer import ObjectDetector
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz

def main():
    frame_prefix = "frame_0"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")

    detector = ObjectDetector() # provide image to model
    
    detector.run(img) # Run model on image

    # The following get the model outputs for each of the detections

    claw = detector.get_claw()
    base = detector.get_base()
    obj = detector.get_object()
    detections = [claw, base, obj]
    print("demonstrating getting the detections from the detector class:\n")
    for det in detections:
        print(f"{det.label} Score: {det.score}")
        input()
    
    # Use the visualizer to show the image, boxes, masks, and the center points

    viz.show_img(img) # Show the image

    rectangles = viz.get_rectangles([claw.box, base.box, obj.box])
    viz.show_img_boxes(img, rectangles)

    viz.show_mask_overlay(img, claw.get_bool_mask(), "Claw mask")
    claw_center = claw.get_center_pixel()
    viz.show_point(img, claw_center, f"Claw Center Point Coordinates: {claw_center}")

    viz.show_mask_overlay(img, base.get_bool_mask(), "Base mask")
    base_center = base.get_center_pixel()
    viz.show_point(img, base_center, f"Base Center Point Coordinates: {base_center}")

    viz.show_mask_overlay(img, obj.get_bool_mask(), "Object mask")
    obj_center = obj.get_center_pixel()
    viz.show_point(img, obj_center, f"Object Center Point Coordinates: {obj_center}")

    # print Claw, Base, and Object depths

    claw_depth = claw.get_average_depth(depth_arr)
    base_depth = base.get_average_depth(depth_arr)
    obj_depth = obj.get_average_depth(depth_arr)

    print(f"Claw Average Depth: {claw_depth}")
    input()
    print(f"Base Average Depth: {base_depth}")
    input()
    print(f"Object Average Depth: {obj_depth}")
    input()

if __name__ == "__main__":
    main()
