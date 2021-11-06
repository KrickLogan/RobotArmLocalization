from math import radians, tan
from DetectedObject import DetectedObject
from ObjectDetector import ObjectDetector
import Utilities.utils as utils
import sys
from Localizer import Localizer
from inspect import currentframe, getframeinfo
import Utilities.visualizer as viz
from Vector import Vector



'''
Example usage of system

localizer = Localizer(img, depth_arr)
target_vector = localizer.get_target_vector()

'''
def get_img_depth(frame_prefix):
    # would really be like "take picture"
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    return img, depth_arr



def main(frame_prefix):

    img, depth_arr = get_img_depth(frame_prefix)

    localizer = Localizer(img, depth_arr)

    print(localizer.detector.get_size())
    claw = localizer.get_claw()[0]#Need to error check at detection level to elimiate possibility of getting this far with multiple detections for a class
    base = localizer.get_base()[0]
    object = localizer.get_object()[0]

    rectangles = viz.get_rectangles([claw.box])
    viz.show_img_boxes(img, rectangles)
    claw_center = claw.get_center_pixel()
    viz.show_point(img, claw_center, f"{claw_center}")

    rectangles = viz.get_rectangles([base.box])
    viz.show_img_boxes(img, rectangles)
    base_center = base.get_center_pixel()
    viz.show_point(img, base_center, f"{base_center}")

    rectangles = viz.get_rectangles([object.box])
    viz.show_img_boxes(img, rectangles)
    object_center = object.get_center_pixel()
    viz.show_point(img, object_center, f"{object_center}")

    
    print(f"Claw Center: {claw_center}")
    print(f"Base Center: {base_center}")

    print(f"Object Center: {object_center}")
    img_width, img_height = img.size
    print(f"\n\nImage Height: {img_height} Width: {img_width}")
    img_center_pxl = (img_width/2, img_height/2) #need to fix, y pixels in image are upside down
    print(f"Image Center: {img_center_pxl}")
    input()
    print("y values are 'upside down' ie values go bottom to top, high to low, so take difference with img height")
    claw_center = (claw_center[0], 1080 - claw_center[1])
    base_center = (base_center[0], 1080 - base_center[1])
    object_center = (object_center[0], 1080 - object_center[1])
    input()
    print("\nnew oject mappings")
    print(f"Claw Center: {claw_center}")
    print(f"Base Center: {base_center}")

    print(f"Object Center: {object_center}")
    input()
    print(f"translate center points so that the origin is now the camera position")
    print("obj cener points - img center")
    claw_center = (claw_center[0] - img_center_pxl[0], claw_center[1] - img_center_pxl[1])
    base_center = (base_center[0] - img_center_pxl[0], base_center[1] - img_center_pxl[1])
    object_center = (object_center[0] - img_center_pxl[0], object_center[1] - img_center_pxl[1])
    input()
    print("\nnew oject mappings")
    print(f"Claw Center: {claw_center}")
    print(f"Base Center: {base_center}")

    print(f"Object Center: {object_center}")
    input()
    print("Blender")
    input()



    # All of this is actually in localizer.to_vector()
    print("\nDepth Value of claw")
    
    claw_depth = claw.get_average_depth(depth_arr)
    print(claw_depth)
    input()
    
    print("\nDepth Value of Base")
    
    base_depth = base.get_average_depth(depth_arr)
    print(base_depth)
    input()

    print("\nDepth Value of Object")
    
    object_depth = object.get_average_depth(depth_arr)
    print(object_depth)

    input()
    print("\n\nGet vertical and Horizontal field of view")
    input()
    vertical_fov = utils.get_vfov()
    horiz_fov = utils.get_hfov()
    
    print(f"\n\nHorizontal and Vertical FOV: {horiz_fov}, {vertical_fov}")
    input()

    # xy_plane_angle, zy_plane_angle = localizer.get_angles_between_pixels(obj_center_pxl, img_center_pxl, vertical_fov, horiz_fov)
    
    obj_x, obj_z = claw_center
    # img_x, img_z = img_center_pxl
    print("Calculate angle in x and z direction by ")
    xy_plane_angle = (obj_x)*(horiz_fov)/(img_width)
    print(f"xy_plane_angle = ({obj_x})*({horiz_fov})/({img_width})")
    zy_plane_angle = (obj_z)*(vertical_fov)/(img_height)
    print(f"zy_plane_angle = ({obj_z})*({vertical_fov})/({img_height})")
    input()
    
    print(f"\n\nXY Plane Angle: {xy_plane_angle}, ZY Plane Angle: {zy_plane_angle}")
    input()
    y = claw_depth
    x = y * tan(radians(xy_plane_angle))
    z = y * tan(radians(zy_plane_angle))
    claw_vector = Vector(x,y,z)
    
    print("\ny = claw_depth",
    "\nx = y * tan(radians(xy_plane_angle))",
    "\nz = y * tan(radians(zy_plane_angle))",
    "\nclaw_vector = Vector(x,y,z)")
    
    print(f"Claw Vector: {claw_vector}")
    input()
    base_vector = localizer.to_vector(base)
    print(f"Base Vector: {base_vector}")
    input()
    object_vector = localizer.to_vector(object)
    print(f"Object Vector: {object_vector}")
    input()

    # target_vector = localizer.get_target_vector() #returns the vector from the RA base to the object

    #for now will just do the calculations of cl_vec - base_vec. will eventually be handled in vector class
    claw_target_vector = Vector(claw_vector.x - base_vector.x, claw_vector.y - base_vector.y,
            claw_vector.z - base_vector.z)

    object_target_vector = Vector(object_vector.x - base_vector.x, object_vector.y - base_vector.y,
            object_vector.z - base_vector.z)

    print(f"Claw Target Vector: {claw_target_vector}")

    print(f"Object Target Vector: {object_target_vector}")



if __name__ == "__main__":
    main(sys.argv[1])
