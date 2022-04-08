
from arm_localizer import ObjectDetector
from arm_localizer import DetectedObject
from arm_localizer import Localizer

import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz
import matplotlib.pyplot as plt
from PIL import ImageOps

def main():
    frame_prefix = "frame_20"
    img = utils.load_image(frame_prefix + ".png")
    plt.imshow(img)
    plt.show()

    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")


    
    detector = ObjectDetector() # provide image to model

    detector.run(img) # Run model on image

    # The following get the model outputs for each of the detections

    claw = detector.get_claw()
    base = detector.get_base()
    obj = detector.get_object()
    bmask = claw.get_bool_mask()

    viz.show_mask_overlay(img=depth_arr, mask=bmask, title="Depth Values of base", depth_arr=depth_arr, force_contrast=True)

    viz.show_depth_distribution(claw, depth_arr, "with outlier")

    claw_depth = claw.get_average_depth(depth_arr)
    base_depth = base.get_average_depth(depth_arr)
    obj_depth = obj.get_average_depth(depth_arr)

    print(f"Claw Depth: {claw_depth}")
    print(f"Base Depth: {base_depth}")
    print(f"Object Depth: {obj_depth}")

if __name__ == "__main__":
    main()
