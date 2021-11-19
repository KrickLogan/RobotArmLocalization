from math import radians, tan
import Utilities.utils as utils
import sys
from Localizer import Localizer
import Utilities.visualizer as viz
from Vector import Vector
import torch
import numpy as np

'''
Example usage of system

'''
def get_img_depth(frame_prefix):
    img = utils.load_image(frame_prefix + ".png")
    depth_arr = utils.load_depth_arr(frame_prefix + "_depth.npy")
    return img, depth_arr

def calculate_base_diameter(vector_left: Vector, vector_right: Vector ) -> float:
    vector_base_diameter = vector_right - vector_left
    base_diameter = Vector.magnitude(vector_base_diameter)
    return base_diameter

def get_angles_between_pixels(obj_center_pxl, img_dims, vertical_fov, horiz_fov) -> float:
    obj_x, obj_z = obj_center_pxl
    img_width, img_height = img_dims
    xy_plane_angle = (obj_x)*(horiz_fov)/(img_width)
    zy_plane_angle = (obj_z)*(vertical_fov)/(img_height)
    return xy_plane_angle, zy_plane_angle

def normalize_pixel_value(obj_pxl, img_center_pxl):
    #translates pixel coordinates so that y axis is standard (bottom to top, low to high) and so origin is moved to image center
    obj_pxl = (obj_pxl[0], 1080 - obj_pxl[1])
    return (obj_pxl[0] - img_center_pxl[0], obj_pxl[1] - img_center_pxl[1])

def to_vector(img, depth, obj_pxl) -> Vector:
    width, height = img.size
    img_dims = (width, height)
    img_center_pxl = (width/2, height/2)
    
    obj_pxl = normalize_pixel_value(obj_pxl, img_center_pxl)
    
    vertical_fov = utils.get_vfov()
    horiz_fov = utils.get_hfov()
    xy_plane_angle, zy_plane_angle = get_angles_between_pixels(obj_pxl, img_dims, vertical_fov, horiz_fov)
    
    y = depth
    x = y * tan(radians(xy_plane_angle))
    z = y * tan(radians(zy_plane_angle))
    return Vector(x,y,z)

def get_base_side_points(base_bool_mask, base_center_y_value):
    indice = torch.tensor([base_center_y_value])
    centerpoint_row = torch.index_select(base_bool_mask, 0, indice).numpy()
    
    true_px_values = []
    counter = 0
    for i in np.nditer(centerpoint_row):
        if i == True:
            true_px_values.append(counter)
        counter += 1

    base_left_side_x = min(true_px_values)
    base_right_side_x = max(true_px_values)
    print(f'base_left_side_x: {base_left_side_x}, base_right_side_x: {base_right_side_x}')

    return base_left_side_x, base_right_side_x

def main(frame_prefix):
    # get img and depth_arr
    img, depth_arr = get_img_depth(frame_prefix)

    # runs model and gets all detected objects
    localizer = Localizer(img, depth_arr)

    # gets base info
    base = localizer.get_base()[0]
    base_center = base.get_center_pixel()
    base_center_y_value = round(base_center[1])
    base_bool_mask = base.get_bool_mask()
    base_left_side_x, base_right_side_x = get_base_side_points(base_bool_mask, base_center_y_value)

    # gets the depth values for the sides of the base
    # WARNING: since the depth arrays contain some 0 values
    #          base_left_depth and base_right_depth may return 0 as well.
    base_left_depth = depth_arr[base_center_y_value, base_left_side_x]
    base_right_depth = depth_arr[base_center_y_value, base_right_side_x]
    print(f'base_left_depth: {base_left_depth}, base_right_depth: {base_right_depth}')

    # gets the average depth of the base's mask
    avg_depth = utils.get_avg_depth(base_bool_mask, depth_arr)
    print(f'avg_depth: {avg_depth}')

    # creates vectors from the camera to each side of the base mask
    vector_left = to_vector(img, 455, (base_left_side_x, base_center_y_value))
    vector_right = to_vector(img, 485, (base_right_side_x, base_center_y_value))

    # calculates the diameter of the base
    calculated_diameter = calculate_base_diameter(vector_left, vector_right)
    print(f'\nCalculated Base Diameter: {calculated_diameter}')

    # compare the calculated base diameter to the known base diameter
    KNOWN_DIAMETER = 98.0
    calculated_error = calculated_diameter - KNOWN_DIAMETER
    print(f'Known Base Diameter: {KNOWN_DIAMETER}')
    print(f'Calculation vs Known Difference: {calculated_error}')

    # # shows mask of the base
    # viz.show_mask_overlay(img, base_bool_mask, 'Base Mask', False, depth_arr)
    
    # # shows depth and mask of the base
    # viz.show_mask_overlay(depth_arr, base_bool_mask, 'Depth and Base Mask', True, depth_arr)

    # # shows centerpoint of the base
    # viz.show_point(img, base_center, f'Centerpoint: {round(base_center[0], 2), round(base_center[1], 2)}')

    # shows left and right points of the base and the base mask
    left_point, right_point = [base_left_side_x, base_center_y_value], [base_right_side_x, base_center_y_value]
    points = [left_point, right_point]
    points_title = f'Calculated Base Diameter: {round(calculated_diameter, 2)}mm\nKnown Base Diameter: {KNOWN_DIAMETER}mm\nCalculated vs Known Difference: {abs(round(calculated_error, 2))}mm'
    viz.show_points(img, points, points_title, base_bool_mask)

if __name__ == "__main__":
    main(sys.argv[1])
