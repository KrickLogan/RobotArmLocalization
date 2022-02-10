
from ObjectDetector import ObjectDetector
from DetectedObject import DetectedObject
from Localizer import Localizer
import Utilities.utils as utils
import Utilities.visualizer as viz
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
    bmask = claw.get_bool_mask()

    viz.show_mask_overlay(img=depth_arr, mask=bmask, title="Depth Values of claw", depth_arr=depth_arr, force_contrast=True)
    data_lables,data_values = viz.get_graph_labels_values(base.get_masked_array(depth_arr))
    viz.show_bar_graph(data_lables,data_values,"with outlier")
    
    claw_depth = claw.get_average_depth(depth_arr)
    base_depth = base.get_average_depth(depth_arr)
    obj_depth = obj.get_average_depth(depth_arr)

    print(f"Claw Depth: {claw_depth}")
    input()
    print(f"Base Depth: {base_depth}")
    input()
    print(f"Object Depth: {obj_depth}")
    input()

    

if __name__ == "__main__":
    main()
