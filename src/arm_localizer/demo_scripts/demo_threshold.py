# This file is used for demonstrating the model
# as it stands on 2/20/2022

from arm_localizer import ObjectDetector

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
    
    # Use the visualizer to show the image, boxes, masks, and the center points

    viz.show_img(img) # Show the image

    # Claw Thresholds

    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold (default)")

    claw.set_threshold(0.10)
    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold")

    claw.set_threshold(0.25)
    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold")

    claw.set_threshold(0.75)
    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold")

    claw.set_threshold(0.90)
    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold")

    # Base Thresholds

    viz.show_mask_overlay(img, base.get_bool_mask(), f"Base mask with {base.get_threshold()} threshold (default)")
    
    base.set_threshold(0.25)
    viz.show_mask_overlay(img, base.get_bool_mask(), f"Base mask with {base.get_threshold()} threshold")
    
    base.set_threshold(0.75)
    viz.show_mask_overlay(img, base.get_bool_mask(), f"Base mask with {base.get_threshold()} threshold")

    # Object Thresholds

    viz.show_mask_overlay(img, obj.get_bool_mask(), f"Object mask with {obj.get_threshold()} threshold (default)")

    obj.set_threshold(0.25)
    viz.show_mask_overlay(img, obj.get_bool_mask(), f"Object mask with {obj.get_threshold()} threshold")

    obj.set_threshold(0.75)
    viz.show_mask_overlay(img, obj.get_bool_mask(), f"Object mask with {obj.get_threshold()} threshold")

    # Invalid Input Tests

    obj.set_threshold(0.5)
    print('\nSetting threshold value to: 0.5')

    print('\nAttempting to set threshold value to: 1')
    obj.set_threshold(1)
    print(f'threshold value is: {obj.get_threshold()}')

    print('\nAttempting to set threshold value to: 0')
    obj.set_threshold(0)
    print(f'threshold value is: {obj.get_threshold()}\n')

if __name__ == "__main__":
    main()
