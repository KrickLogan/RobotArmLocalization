import DetectedObject
import ObjectDetector
import Utilities.utils as utils
import sys


HFOV = 50 #degrees
VFOV = 35 #degrees


def main(frame_prefix, sys_base_to_claw):
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    
    detector = ObjectDetector(img, depth_arr)
    detections = detector.run()
    claw = None
    cotton = None
    base = None
    for obj in detections:
        center_pxl = utils.get_center_point(obj["box"])
        depth = utils.get_avg_depth(utils.get_bool_mask(obj["mask"]), depth_arr)
        coordinates = utils.calculate_vector(center_pxl, depth, HFOV, VFOV)
        label = utils.get_label_string(obj["label"])
        
        if label == utils.CLAW_STRING:
            claw = Vector(coordinates) #Vector class
        elif label == utils.COTTON_STRING:
            cotton = Vector(coordinates)
        elif label == utils.BASE_STRING:
            base = Vector(coordinates)
        else:
            print(label)

    if claw is not None and base is not None and cotton is not None:
        base_to_claw = claw - base #Vector Class
        rotation_angle = base_to_claw.get_angle_between(sys_base_to_claw) # Vector class
        base_to_cotton = cotton - base
        base_to_cotton = base_to_cotton.rotate(rotation_angle) #Vector class
    





if __name__ == "__main__":
    main(sys.argv[1])