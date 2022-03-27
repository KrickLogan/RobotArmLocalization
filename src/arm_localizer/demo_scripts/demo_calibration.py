import matplotlib.pyplot as plt
from arm_localizer import *
from arm_localizer import visualizer as viz
from math import radians, degrees
from PIL import Image
import os

def get_center_points(detector):
    points = []
    for d in detector.get_all_detections():
        p = d.get_center_mass_pixel()
        points.append(p)
    return points

def show_all_detections(img, depth_arr, detector):
    # for d in detector.get_all_detections():
    #     viz.show_mask_overlay(img, d.get_bool_mask(), "detection")
    #     viz.show_mask_overlay(depth_arr, d.get_bool_mask(), "detection", force_contrast=True, depth_arr=depth_arr)
    
    viz.show_mask_overlay(img, detector.get_claw().get_bool_mask(), "claw detection")
    viz.show_mask_overlay(img, detector.get_base().get_bool_mask(), "Base Detection")
    viz.show_mask_overlay(img, detector.get_object().get_bool_mask(), "Object Detection")
    
    # viz.show_mask_overlay(depth_arr, detector.get_claw().get_bool_mask(), "claw detection", force_contrast=True, depth_arr=depth_arr)
    # viz.show_mask_overlay(depth_arr, detector.get_base().get_bool_mask(), "Base Detection", force_contrast=True, depth_arr=depth_arr)
    # viz.show_mask_overlay(depth_arr, detector.get_object().get_bool_mask(), "Object Detection", force_contrast=True, depth_arr=depth_arr)


    viz.show_img_boxes(img, [detector.get_claw().box, detector.get_base().box, detector.get_object().box])

    center_points = get_center_points(detector)
    # print(center_points)
    viz.show_points(img, center_points, "Center Points")

def show_all_vectors(cam_claw_1, cam_claw_2, pos_claw_1, pos_claw_2, cam_obj, pos_obj, og, norm=None):
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
    
    og = Vector(0,0,0)

    pos_claw_1 = Vector(247, 110, 211)
    pos_claw_2 = Vector(268, -90, 173)

    pos_obj = Vector(439, -202, -22)
    pos_obj2 = Vector(245, 202, -22)
    pos_obj3 = Vector(459, 78, 205)

    camera_position = "position_1"
    # camera_position = 'position_2'
    # camera_position = 'position_3'
    # camera_position = 'position_3b'
    # camera_position = 'position_4'
    # camera_position = 'position_5'
    # camera_position = 'position_6'
    
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
