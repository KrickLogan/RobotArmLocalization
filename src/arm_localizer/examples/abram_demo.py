## Run calibrate.py before running

from arm_localizer import *
from PIL import Image
from matplotlib import pyplot as plt
import os
import numpy as np
from math import degrees


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


    # These are the positions of the claws, in positions 1 and 2, in millimeters, 
    # relative to the Robot arm's coordinate system
    pos_claw_1 = Vector(247, 110, 211)
    pos_claw_2 = Vector(268, -90, 173)

    # These are the positions of the objects, in positions 1, 2, and 3, in millimeters, 
    # relative to the Robot arm's coordinate system
    pos_obj1 = Vector(439, -202, -22)
    pos_obj2 = Vector(245, 202, -22)
    pos_obj3 = Vector(459, 78, 205)



    object_positions = [pos_obj1, pos_obj2, pos_obj3]


    #You can run the script on different camera positions by uncommenting the various positions

    camera_position = "position_1"
    # camera_position = 'position_2'
    # camera_position = 'position_3'
    # camera_position = 'position_4'
    # camera_position = 'position_5'
    # camera_position = 'position_6'
    
    detector = ObjectDetector()

    #load claw 1
    frame_prefix = 'claw_1'
    img1 = Image.open(os.path.join("camera_data", camera_position, "images", f"{frame_prefix}.png")).convert("RGB")

    depth_arr1 = np.load(os.path.join("camera_data",  camera_position, "depths", f"{frame_prefix}_depth.npy"))
    
    detector.run(img1)
    cam_claw1 = detector.get_claw().rs_to_vector(depth_arr1) - detector.get_base().rs_to_vector(depth_arr1)
    
    #load claw 2
    file_names=['claw_2', 'obj_2', 'obj_3']
    obj_position = 0
    frame_prefix = file_names[obj_position]
    object_positions = [pos_obj1, pos_obj2, pos_obj3]
    pos_obj = object_positions[obj_position]

    img2 = Image.open(os.path.join("camera_data", camera_position, "images", f"{frame_prefix}.png")).convert("RGB")
    depth_arr2 = np.load(os.path.join("camera_data", camera_position, "depths",  f"{frame_prefix}_depth.npy"))
    
    # plt.imshow(img)
    # plt.show()

    detector.run(img2)

    cam_claw2 = detector.get_claw().rs_to_vector(depth_arr2) - detector.get_base().rs_to_vector(depth_arr2)
    cam_obj = detector.get_object().rs_to_vector(depth_arr2) - detector.get_base().rs_to_vector(depth_arr2)
    
    show_all_vectors(cam_claw_1=cam_claw1, cam_claw_2=og, pos_claw_1=pos_claw_1, pos_claw_2=og, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

    rs_calibrate(img1, depth_arr1, img2, depth_arr2, pos_claw_1, pos_claw_2)

    l = Localizer()

    print('apply first rotation')
    
    cam_claw1 = cam_claw1.rotate_about_vector(l.rotation._f_rot_vector, l.rotation._f_rot_rads)
    cam_obj = cam_obj.rotate_about_vector(l.rotation._f_rot_vector, l.rotation._f_rot_rads)
    

    print("\nNote that at this point, the camera object and position object vectors are not aligned, we need more information which we will get from",
        "a second set of claw data.")

    show_all_vectors(cam_claw_1=cam_claw1, cam_claw_2=og, pos_claw_1=pos_claw_1, pos_claw_2=og, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

    
    
    show_all_vectors(cam_claw_1=cam_claw1, cam_claw_2=cam_claw2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

    print("apply first rotation to second claw vector")
    cam_claw2 = cam_claw2.rotate_about_vector(l.rotation._f_rot_vector, l.rotation._f_rot_rads)
    
    show_all_vectors(cam_claw_1=cam_claw1, cam_claw_2=cam_claw2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

    print('apply second rotation to second claw')

    cam_claw1 = cam_claw1.rotate_about_vector(l.rotation._s_rot_vector, l.rotation._s_rot_rads)
    cam_claw2 = cam_claw2.rotate_about_vector(l.rotation._s_rot_vector, l.rotation._s_rot_rads)
    
    show_all_vectors(cam_claw_1=cam_claw1, cam_claw_2=cam_claw2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

    print("apply second rotation to the cam object vector to finally calculate the coordinates of the object in the robot arm's coordinate system.")

    cam_obj = cam_obj.rotate_about_vector(l.rotation._s_rot_vector, l.rotation._s_rot_rads)

    
    print("\n\nAll vector coordinates and measurements are in millimeters")
    print(f"Calculated Position Vector: {cam_obj}\nActual Position Vector: {pos_obj}\n")
    cmag = round(cam_obj.magnitude())
    pmag = round(pos_obj.magnitude())
    print(f"Magnitudes\nCalculation: {cmag}\nActual: {pmag}\n")
    print(f"Angle Between: {round(degrees(cam_obj.angle_between(pos_obj)))}\n")
    e = pos_obj - cam_obj
    print(f"Error Vector: {e}, Magnitude: {round(e.magnitude())}")

    show_all_vectors(cam_claw_1=cam_claw1, cam_claw_2=cam_claw2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)


if __name__ == "__main__":
    main()




