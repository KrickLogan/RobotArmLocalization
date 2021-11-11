import DetectedObject
import ObjectDetector
import Utilities.utils as utils
import sys
import Localizer
from inspect import currentframe, getframeinfo



'''Example usage'''
def get_img_depth(frame_prefix):
    #would really be like "take picture"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    return img, depth_arr

def get_claw_position():
    #sys call to get the position of the claw from the positioning system
    return (.5, .5, .5)

def move_claw_to_object(object_coordinates):
    #system call to move the claw to the target position
    return



def main(frame_prefix):

    img, depth_arr = get_img_depth(frame_prefix)

    true_claw_position = get_claw_position()
    
    localizer = Localizer(img, depth_arr)

    localizer.calibrate_coordinate_system(true_claw_position) # Correct the positioning of the localizer to the true claw position from the positioning system

    target_vector = localizer.get_target_vector() #returns the vector from the RA base to the object
    
    move_claw_to_object(target_vector.to_coords())
    









    # height, width = img.size 
    # img_center = (width/2, height/2)
    # depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    
    # detector = ObjectDetector(img)
    # detections = detector.run()
    # claw = None
    # cotton = None
    # base = None
    # for obj in detections:
    #     box_center = utils.get_center_point(obj["box"])
    #     depth = utils.get_avg_depth(utils.get_bool_mask(obj["mask"]), depth_arr)
    #     coordinates = utils.calculate_vector(box_center, img_center, depth)
    #     label = utils.get_label_string(obj["label"])
        
    #     if label == utils.CLAW_STRING:
    #         claw = Vector(coordinates) #Vector class
    #     elif label == utils.COTTON_STRING:
    #         cotton = Vector(coordinates)
    #     elif label == utils.BASE_STRING:
    #         base = Vector(coordinates)
    #     else:
    #         print(label)

    # if claw is not None and base is not None and cotton is not None:
    #     base_to_claw = claw - base #Vector Class
    #     rotation_angle = base_to_claw.get_angle_between(sys_base_to_claw) # Vector class
    #     base_to_cotton = cotton - base
    #     base_to_cotton = base_to_cotton.rotate(rotation_angle) #Vector class
    #     return base_to_cotton





if __name__ == "__main__":
    main(sys.argv[1])