from arm_localizer import *
from arm_localizer import visualizer as viz
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from math import degrees

def get_center_points(detector):
    points = []
    dets = [detector.get_claw(), detector.get_object(), detector.get_base()]
    for d in dets:
        p = d.get_center_mass_pixel()
        points.append(p)
    return points


def show_all_detections(img, depth_arr, detector):
    # for d in detector.get_all_detections():
    #     viz.show_mask_overlay(img, d.get_bool_mask(), "detection")
    #     viz.show_mask_overlay(depth_arr, d.get_bool_mask(), "detection", force_contrast=True, depth_arr=depth_arr)
    
    viz._show_mask_overlay(img, detector.get_claw().get_bool_mask(), "claw detection")
    viz._show_mask_overlay(img, detector.get_base().get_bool_mask(), "Base Detection")
    viz._show_mask_overlay(img, detector.get_object().get_bool_mask(), "Object Detection")
    
    viz._show_mask_overlay(depth_arr, detector.get_claw().get_bool_mask(), "claw detection", force_contrast=True, depth_arr=depth_arr)
    viz._show_mask_overlay(depth_arr, detector.get_base().get_bool_mask(), "Base Detection", force_contrast=True, depth_arr=depth_arr)
    viz._show_mask_overlay(depth_arr, detector.get_object().get_bool_mask(), "Object Detection", force_contrast=True, depth_arr=depth_arr)

    rectangles = viz.get_rectangles([detector.get_claw().box, detector.get_base().box, detector.get_object().box])
    viz.show_img_boxes(img, rectangles)

    center_points = get_center_points(detector)
    # print(center_points)
    viz._show_points(img, center_points, "Center Points")

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

    pos_obj1 = Vector(439, -202, -22)
    pos_obj2 = Vector(245, 202, -22)
    pos_obj3 = Vector(459, 78, 205)

    object_positions = [pos_obj1, pos_obj2, pos_obj3]
    
    camera_position = "position_1"
    # camera_position = 'position_2'
    # camera_position = 'position_3'
    # camera_position = 'position_3b'
    # camera_position = 'position_4'
    # camera_position = 'position_5'
    # camera_position = 'position_6'
    
    detector = ObjectDetector()
    file_names=['claw_2', 'obj_2', 'obj_3']
    object_positions = [pos_obj1, pos_obj2, pos_obj3]

    for obj_position in range(3):
        
        frame_prefix = file_names[obj_position]
        pos_obj = object_positions[obj_position]


        img = Image.open(os.path.join("camera_data","images", '3_15_22', camera_position, f"{frame_prefix}.png")).convert("RGB")

        depth_arr = np.load(os.path.join("camera_data", "depths", "3_15_22", camera_position, f"{frame_prefix}_depth.npy"))

        detector.run(img)

        obj_vector = detector.get_object().rs_to_vector(depth_arr) - detector.get_base().rs_to_vector(depth_arr)
        show_all_vectors(cam_claw_1=Vector(0,0,0), cam_claw_2=Vector(0,0,0), pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=obj_vector, pos_obj=pos_obj, og=og)

        l = Localizer()

        calculated_position = l.get_real_position(obj_vector)

        print("\n\nAll vector coordinates and measurements are in millimeters")
        print(f"Calculated Position Vector: {calculated_position}\nActual Position Vector: {pos_obj}\n")
        cmag = round(calculated_position.magnitude())
        pmag = round(pos_obj.magnitude())
        print(f"Magnitudes\nCalculation: {cmag}\nActual: {pmag}\n")
        print(f"Angle Between: {round(degrees(calculated_position.angle_between(pos_obj)))}\n")
        e = pos_obj - calculated_position
        print(f"Error Vector: {e}, Magnitude: {round(e.magnitude())}")
        print(f"Net Magnitude error: {abs(round(e.magnitude()) - abs(pmag - cmag))}")

        show_all_vectors(cam_claw_1=Vector(0,0,0), cam_claw_2=Vector(0,0,0), pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=calculated_position, pos_obj=pos_obj, og=og)

        if input("show detections? ") != 'n':
            show_all_detections(img, depth_arr, detector)


if __name__ == "__main__":
    main()
