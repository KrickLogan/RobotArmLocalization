from arm_localizer import ObjectDetector
import arm_localizer.utilities.utils as utils
import matplotlib.pyplot as plt
import arm_localizer.utilities.visualizer as viz


# This file demonstrates more advanced usage of the system. It lets the user directly
# interact with the model, submitting images, and manipulating the model outputs/detections
# Throughout the project, it became apparent that there is a great need for interactive 
# trouble shooting and thats what this file attempts to show. Errors in the positions can 
# be attributed to poor model outputs and this file shows how you can evaluate the images to
# determine the source of error. For visualizations, see demo_visualizer.py 
# 
#  


def main():
    frame_prefix = "frame_20"   
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    plt.imshow(img)
    plt.show()

    # provide image to model
    detector = ObjectDetector()
    
    # run model on provided image
    detector.run(img) 

    # The following get the output of all detections
    detections = detector.get_all_detections()
    for det in detections:
        print(f"{det.label} Score: {det.score} Box: {det.box} Mask: {det.mask}" )

    # The following prints all model outputs
    output = detector.get_model_outputs()
    print (output)

    claw = detector.get_claw()
    print (f"label: {claw.label} Score: {claw.score} Box: {claw.box} Mask: {claw.mask} Average depth: {claw.get_depth(claw.get_masked_array(depth_arr))}")

    base = detector.get_base()
    print (f"label: {base.label} Score: {base.score} Box: {base.box} Mask: {base.mask} Average depth: {base.get_depth(base.get_masked_array(depth_arr))}")

    obj = detector.get_object()
    print (f"label: {obj.label} Score: {obj.score} Box: {obj.box} Mask: {obj.mask} Average depth: {obj.get_depth(obj.get_masked_array(depth_arr))}")
    
if __name__ == "__main__":
    main()
