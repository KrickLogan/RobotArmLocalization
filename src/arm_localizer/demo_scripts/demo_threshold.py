# This file is used for demonstrating the model
# as it stands on 2/20/2022

from arm_localizer import ObjectDetector

import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz

def main():
    frame_prefix = "frame_0"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")

    # Test Invalid thresholds for ObjectDetector
    print('\nAttempting to initialize ObjectDetector with INVALID threshold values: 0, 1, 2')
    detector = ObjectDetector(threshold_claw = 0, threshold_base = 1, threshold_object = 2)

    detector.run(img) # Run model on image

    # Test Valid thresholds for ObjectDetector
    input()

    print('\nAttempting to initialize ObjectDetector with VALID threshold values: 0.123, 0.456, 0.789')
    detector = ObjectDetector(threshold_claw = 0.123, threshold_base = 0.456, threshold_object = 0.789)

    detector.run(img) # Run model on image

    # The following get the model outputs for each of the detections

    claw = detector.get_claw()
    base = detector.get_base()
    obj = detector.get_object()
    
    # Print Threshold Values of each detection
    input()

    print('\nThresholds Initialized from ObjectDetector:')
    print(f'Claw Threshold: {claw.get_threshold()}')
    print(f'Base Threshold: {base.get_threshold()}')
    print(f'Object Threshold: {obj.get_threshold()}')

    # Set Thresholds back to default (0.5)

    claw.set_threshold(0.5)
    base.set_threshold(0.5)
    obj.set_threshold(0.5)

    # Print Threshold Values of each detection
    input()

    print('\nSet Thresholds back to default (0.5):')
    print(f'Claw Threshold: {claw.get_threshold()}')
    print(f'Base Threshold: {base.get_threshold()}')
    print(f'Object Threshold: {obj.get_threshold()}')
    
    # Use the visualizer to show the image, boxes, masks, and the center points
    input()

    viz.show_img(img) # Show the image

    # Claw Thresholds

    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold (default)")

    claw.set_threshold(0.25)
    viz.show_mask_overlay(img, claw.get_bool_mask(), f"Claw mask with {claw.get_threshold()} threshold")

    claw.set_threshold(0.75)
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
    input()

    obj.set_threshold(0.5)
    print('\nSet Thresholds back to default (0.5):')

    print('\nAttempting to set threshold value to: 1')
    obj.set_threshold(1)
    print(f'threshold value is: {obj.get_threshold()}')

    print('\nAttempting to set threshold value to: 0')
    obj.set_threshold(0)
    print(f'threshold value is: {obj.get_threshold()}\n')

if __name__ == "__main__":
    main()
