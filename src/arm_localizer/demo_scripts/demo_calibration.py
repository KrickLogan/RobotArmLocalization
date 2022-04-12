import matplotlib.pyplot as plt
from arm_localizer import *
from arm_localizer import visualizer as viz
from math import radians, degrees
from PIL import Image
import os

    
def get_center_points(detector):
    """Gets a list of center points

    This function returns all of the center points from the ObjectDetector in the form of a list.
    1. Obtain the list of DetectedObjects from the model outputs, instances of classifications
    2. Initialize p with a value of the untransformed pixel value coordinates representing DetectedObjects calculated center of mass
    3. Add center of mass point to the list of points    

    Args:
        detector (ObjectDetector): returns the model detections 
    
    returns:
        points: Returns a list of the points representing the DetectedObjects center of mass

    """
    points = []    
    for d in detector.get_all_detections():        
        p = d.get_center_mass_pixel()        
        points.append(p)   
    return points

def show_all_detections(img, depth_arr, detector):
    """Show the model detections and mask overlaid

    This function obtains all classifications and shows the detections with the mask overlays. 
    Display the claw.
    Display the base.
    Display the object.
    gets bounding boxes
    gets center points

    Args:
        img (image): rgb data
        depth_arr (np.array): depth array, depths in mm
        detector (ObjectDetector): Provides output from model, classifications

    Returns:
        none

    """
    # for d in detector.get_all_detections():
    #     viz.show_mask_overlay(img, d.get_bool_mask(), "detection")
    #     viz.show_mask_overlay(depth_arr, d.get_bool_mask(), "detection", force_contrast=True, depth_arr=depth_arr)
    
    viz.show_mask_overlay(img, detector.get_claw().get_bool_mask(), "claw detection")
    viz.show_mask_overlay(img, detector.get_base().get_bool_mask(), "Base Detection")
    viz.show_mask_overlay(img, detector.get_object().get_bool_mask(), "Object Detection")
    
    # viz.show_mask_overlay(depth_arr, detector.get_claw().get_bool_mask(), "claw detection", force_contrast=True, depth_arr=depth_arr)
    # viz.show_mask_overlay(depth_arr, detector.get_base().get_bool_mask(), "Base Detection", force_contrast=True, depth_arr=depth_arr)
    # viz.show_mask_overlay(depth_arr, detector.get_object().get_bool_mask(), "Object Detection", force_contrast=True, depth_arr=depth_arr)


    rectangles = viz.get_rectangles([detector.get_claw().box, detector.get_base().box, detector.get_object().box])
    viz.show_img_boxes(img, rectangles)

    center_points = get_center_points(detector)
    # print(center_points)
    viz.show_points(img, center_points, "Center Points")

def show_all_vectors(cam_claw_1, cam_claw_2, pos_claw_1, pos_claw_2, cam_obj, pos_obj, og, norm=None):
    """_summary_

    Args:
        cam_claw_1 (_type_): The position of the claw from the camera 
        cam_claw_2 (_type_): _description_
        pos_claw_1 (Vector): The position of the claw from the Robot arm coordinate system which corresponds to the first depth and img
        pos_claw_2 (Vector): The position of the claw from the Robot arm coordinate system which corresponds to the second depth and img
        cam_obj (_type_): _description_
        pos_obj (_type_): _description_
        og (Vector): The zero vector originating at the origin
        norm (_type_, optional): _description_. Defaults to None.
    """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x,y,z = og.as_point()

    for pt,col in zip([cam_obj, pos_obj],['y','g']):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color=col)
        ax.scatter(a,b,c,marker="^", color='k')

    for pt,col in zip([cam_claw_1, cam_claw_2],['c','m']):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color='b')
        ax.scatter(a,b,c,marker="^", color=col)

    for pt,col in zip([pos_claw_1,pos_claw_2],["c","m"]):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color='r')
        ax.scatter(a,b,c,marker="^", color=col)

    if norm != None:
        a,b,c = norm.as_point()
        ax.plot([x,a],[y,b],[z,c], color='k')
        ax.scatter(a,b,c,marker="^", color='k')
    
    ax.scatter(x,y,z, marker="o")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim([-500,500])
    ax.set_ylim([-500,500])
    ax.set_zlim([-200,500])
    plt.show()

def main():
    """Carries out the execution of the calibration functions

    The main function steps through the individual steps of the calibration process.
    1. loads first and second images: each are done individually and are corresponding to a separate claw position
    2. loads first and second depth arrays: each are done individually and are corresponding to a separate claw position
    3. get actual claw position from positioning system of the robot arm
    4. 

    This function 
    
    """

    # initialize origin with a vector of zero's
    og = Vector(0,0,0)

    # The position of claws initialized with initial vector poisitions (claw to base) in mm
    pos_claw_1 = Vector(247, 110, 211)
    pos_claw_2 = Vector(268, -90, 173)

    # This initializes pos_obj with a vector. Object measured from base in mm.  
    pos_obj = Vector(439, -202, -22)
    # This initializes pos_obj2 with vector of object
    pos_obj2 = Vector(245, 202, -22)
    pos_obj3 = Vector(459, 78, 205)

    # Camera position is initialized as the first postition, postion 1
    camera_position = "position_1"
    # camera_position = 'position_2'
    # camera_position = 'position_3'
    # camera_position = 'position_3b'
    # camera_position = 'position_4'
    # camera_position = 'position_5'
    # camera_position = 'position_6'
    
    # create file_names that contains a list with claw and object values
    file_names=['claw_1', 'claw_2', 'obj_2', 'obj_3']
    frame_prefix = file_names[0]

    img1 = Image.open(os.path.join("camera_data","images", '3_15_22', camera_position, f"{frame_prefix}.png")).convert("RGB")

    # depth_arr1 = utils.load_depth_arr(f"./camera_data/depths/{align_to}/{camera_position}/{frame_prefix}_depth.npy")
    depth_arr1 = np.load(os.path.join("camera_data", "depths", "3_15_22", camera_position, f"{frame_prefix}_depth.npy"))
    
    plt.imshow(img1)
    plt.show()

    frame_prefix = file_names[1]
    img2 = Image.open(os.path.join("camera_data","images", '3_15_22', camera_position, f"{frame_prefix}.png")).convert("RGB")

    # depth_arr1 = utils.load_depth_arr(f"./camera_data/depths/{align_to}/{camera_position}/{frame_prefix}_depth.npy")
    depth_arr2 = np.load(os.path.join("camera_data", "depths", "3_15_22", camera_position, f"{frame_prefix}_depth.npy"))
    
    plt.imshow(img2)
    plt.show()

    rs_calibrate(img1, depth_arr1, img2, depth_arr2, pos_claw_1, pos_claw_2)

    detector = ObjectDetector()

    detector.run(img2)

    show_all_detections(img2, depth_arr2, detector)
    

if __name__ == "__main__":
    main()
