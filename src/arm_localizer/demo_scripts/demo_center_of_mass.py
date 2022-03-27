# This file is used for demonstrating the model
# as it stands on 2/20/2022

from arm_localizer.arm_localizer import ObjectDetector
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz

def main():
    frame_prefix = "frame_20"
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
    
    claw_center_mass_pixel = claw.get_center_mass_pixel()
    claw_center_pixel = claw.get_center_pixel()
    base_center_mass_pixel = base.get_center_mass_pixel()
    base_center_pixel = base.get_center_pixel()
    obj_center_mass_pixel = obj.get_center_mass_pixel()
    obj_center_pixel = obj.get_center_pixel()

    rectangles = viz.get_rectangles([claw.box, base.box, obj.box])
    viz.show_img_boxes(img, rectangles)

    print (f"claw center pixel: {claw_center_pixel}")
    viz.show_point(img, claw_center_pixel, f"Claw Center Point Coordinates (old): {claw_center_pixel}")
    print (f"claw center mass pixel: {claw_center_mass_pixel}")
    viz.show_point(img, claw_center_mass_pixel, f"Claw Center of Mass Point Coordinates (new): {claw_center_mass_pixel}")

    print (f"base center pixel: {base_center_pixel}")
    viz.show_point(img, base_center_pixel, f"Base Center Point Coordinates (old): {base_center_pixel}")
    print (f"base center mass pixel: {base_center_mass_pixel}")
    viz.show_point(img, base_center_mass_pixel, f"Base Center of Mass Point Coordinates (new): {base_center_mass_pixel}")

    print (f"objcenter pixel: {obj_center_pixel}")
    viz.show_point(img, obj_center_pixel, f"Object Center Point Coordinates (old): {obj_center_pixel}")
    print (f"obj center mass pixel: {obj_center_mass_pixel}")
    viz.show_point(img, obj_center_mass_pixel, f"Object Center of Mass Point Coordinates (new): {obj_center_mass_pixel}")

if __name__ == "__main__":
    main()
