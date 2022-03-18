# This file is used for demonstrating the model
# as it stands on 2/20/2022

from arm_localizer.object_detector import ObjectDetector
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz
import pyrealsense2 as rs

def main():
    frame_prefix = "frame_398"
    img = utils.load_image(frame_prefix + ".png")
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
        print(f"{det.label} Score: {det.score}")
    
    # Base Object Deprojection

    base_center_point = base.get_center_mass_pixel()
    base_average_depth = base.get_average_depth()

    # obtain camera intrinsics directly from camera
    _intrinsics = rs.intrinsics()

    result = rs.rs2_deproject_pixel_to_point(_intrinsics, base_center_point, base_average_depth) #possibly (base_center_point, _intrinsics, base_average_depth)

    print(f"result: {result}")

if __name__ == "__main__":
    main()
