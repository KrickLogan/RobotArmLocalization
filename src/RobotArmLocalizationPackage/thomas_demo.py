from math import radians, tan
from DetectedObject import DetectedObject
from ObjectDetector import ObjectDetector
import Utilities.utils as utils
import sys
from Localizer import Localizer
from inspect import currentframe, getframeinfo

from Vector import Vector



'''Example usage of system'''
def get_img_depth(frame_prefix):
    #would really be like "take picture"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    return img, depth_arr



def main(frame_prefix):

    img, depth_arr = get_img_depth(frame_prefix)

    localizer = Localizer(img, depth_arr)

    claw = localizer.get_claw()
    base = localizer.get_base()
    object = localizer.get_object()

    claw_center = claw.get_center_point()
    base_center = base.get_center_point()
    object_center = object.get_center_point()

    print(claw_center)
    print(base_center)
    print(object_center)


    depth = claw.get_average_depth(depth_arr)
    print(depth)
    height, width = img.size
    print(f"Height: {height} Width: {width}")
    img_center_pxl = (width/2, height/2) #need to fix, y pixels in image are upside down
    print(f"Image Center Pixel: {img_center_pxl}")
    obj_center_pxl = claw.get_center_pixel()
    print(f"Object Center Pixel: {obj_center_pxl}")
    vertical_fov = utils.get_vfov
    horiz_fov = utils.get_hfov
    print(f"Horizontal and Vertical FOV: {horiz_fov}, {vertical_fov}")
    xy_plane_angle, zy_plane_angle = localizer.get_angles_between_pixels(obj_center_pxl, img_center_pxl, vertical_fov, horiz_fov)
    print(f"XY Plane Angle: {xy_plane_angle}, ZY Plane Angle: {zy_plane_angle}")
    y = depth
    x = y * tan(radians(xy_plane_angle))
    z = y * tan(radians(zy_plane_angle))
    claw_vector = Vector(x,y,z)

    print(claw_vector)

    base_vector = localizer.to_vector(base)
    print(base_vector)
    object_vector = localizer.to_vector(object)
    print(object_vector)

    target_vector = localizer.get_target_vector() #returns the vector from the RA base to the object
