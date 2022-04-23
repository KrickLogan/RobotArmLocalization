import os
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy.ma as ma
import numpy as np

def maximize_plt():
    """If the OS is Windows, maximizes the plot
    """
    if os.name == 'nt':
        mng = plt.get_current_fig_manager() 
        mng.window.state("zoomed")

def get_label_string(label):
    label_string = ''
    if label == 1:
        label_string = 'Base'
    elif label == 2:
        label_string = 'Claw'
    elif label == 3:
        label_string = 'Cotton'
    elif label == 0:
        label_string = 'Background'
    else:
        label_string = 'Error!'
    return label_string

def show_img(img):
    """Displays an image

    Args:
        img (img): The image to be displayed
    """
    plt.imshow(img)
    plt.title('Original Image')
    maximize_plt()
    plt.show()

def _show_mask_overlay(img, mask, title="", force_contrast=False, depth_arr=None):
    """Displays one mask on top of an image. 

    Args:
        img (img): The image to be displayed
        mask (boolmask): The mask to be overlaid with the image
        title (string): The name of the plot
        force_contrast (boolean): idk
        depth_arr (numpy): The array of depth values in millimeters
    """
    if force_contrast: 
        min = 400
        max = 700

        if depth_arr is not None:
            unique_values = np.unique(ma.masked_array(depth_arr, np.invert(mask).long()))
            
            # print(unique_values)
            max = unique_values[-2]
            min = unique_values[1]

        plt.imshow(img, vmin=min, vmax=max)

    else:
        plt.imshow(img)
    plt.imshow(mask, cmap='ocean', alpha=.5)
    if depth_arr is not None:
        plt.imshow(depth_arr, alpha=0)
    plt.title(title)
    maximize_plt()
    plt.show() 

def show_mask(detection, img, depth= None): 
    """Displays one mask on top of an image. 

    Args:
        img (img): The image to be displayed
        mask (boolmask): The mask to be overlaid with the image
        depth_arr (numpy): The array of depth values in millimeters
    """
    _show_mask_overlay(img=img, mask=detection.get_bool_mask(), title=detection.get_label(), force_contrast=False, depth_arr=depth)

def show_all_masks(detections, img, depth=None):
    plt.imshow(img)

    bool_mask = detections[0].get_bool_mask()
    composite_mask = np.full_like(bool_mask, False)
    
    for detection in detections:
        bool_mask = detection.get_bool_mask()
        composite_mask = np.logical_or(bool_mask, composite_mask)

    _show_mask_overlay(img, composite_mask, title="All masks", force_contrast=False, depth_arr=depth)

def show_center_point (detection, img, title = ""):
    """Displays one center point on top of an image

    Args:
        detection (detectedObject): The object for which to display the center point
        img (img): The image to be displayed
        title (string): The name of the plot
    """
    center_point = detection.get_center_mass_pixel()
    _show_point(img, center_point, title)   

def show_center_points (detections, img, title=""):
    """Displays all center points

    Args:
        detections (detectedObjects): The detections in the image, all of which will have center points displayed.
        img (img): The image to be displayed
        title (string): The name of the plot
    """
    center_points = []
    for detection in detections:
        center_points.append(detection.get_center_mass_pixel())
    _show_points(img, center_points, title)

def _show_point(img, point, title = "", mask = None):
    plt.imshow(img)
    if(mask != None):
        plt.imshow(mask, cmap='ocean', alpha=.5)
    plt.title(title)
    plt.plot(point[0], point[1], 'b*')
    maximize_plt()
    plt.show()

def _show_points(img, points, title = "", mask = None):
    plt.imshow(img)
    if(mask != None):
        plt.imshow(mask, cmap='ocean', alpha=.5)
    plt.title(title)
    for i in range(len(points)):
        point = points[i]
        plt.plot(point[0], point[1], 'r*')

    maximize_plt()
    plt.show()

def show_img_box(detection, img, title = ""):
    """Displays one bounding box on top of an image

    Args:
        detection (detectedObject): The object for which to display the bounding box
        img (img): The image to be displayed
        title (string): The name of the plot
    """
    plt.imshow(img)
    x, y, w, h = detection.box.detach().numpy()
    plt.gca().add_patch(Rectangle((x,y), w - x, h - y, edgecolor='red', fill=False))
    plt.title(title)
    maximize_plt()
    plt.show()

def show_img_boxes(detections, img, title = ""):
    """Displays all bounding boxes

    Args:
        detections (detectedObjects): The detections in the image, all of which will have bounding boxes displayed.
        img (img): The image to be displayed
        title (string): The name of the plot
    """
    plt.imshow(img)
    for d in detections:
        x, y, w, h = d.box.detach().numpy()
        plt.gca().add_patch(Rectangle((x,y), w - x, h - y, edgecolor='red', fill=False))
    plt.title(title)
    maximize_plt()
    plt.show()

def show_depth_distribution(detection, depth, title="", x_axis_label="", y_axis_label=""):
    """Displays the outlier distribution of the depth

    Args:
        detection (detectedObject): The object we are analyzing
        depth (numpy): The array of depth values in millimeters
        title (string): The name of the plot
        x_axis_label (string): The label on the x axis
        y_axis_label (string): The label on the y axis
    """
    ma_depth = detection.remove_depth_outliers(detection.get_masked_depth_array(depth))
    _show_bar_graph(ma_depth, title, x_axis_label, y_axis_label)

def _show_bar_graph(ma_depth, title="", x_axis_label="", y_axis_label=""):
    data_labels, data_values = _get_graph_labels_values(ma_depth)
    label_indices = [i for i, _ in enumerate(data_labels)]
    plt.bar(label_indices, data_values, color="blue")
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.title(title)
    plt.xticks(label_indices, data_labels)
    maximize_plt()
    plt.show()

def _get_graph_labels_values(ma_depth):
    partitions = 6
    unique_values, frequencies = np.unique(ma_depth, return_counts=True)
    
    for i in range(len(unique_values)):   
        if not np.isscalar(unique_values[i]):
            frequencies = np.delete(frequencies, i)
            unique_values = np.delete(unique_values, i)

    # print(f"Percentage 0: {frequencies[0]/frequencies[1:].sum()} ")
    
    frequencies = frequencies[1:]
    unique_values = unique_values[1:]
    
    index_interval = round((unique_values[-1] - unique_values[0])/(partitions))
    
    np_segment_boundaries = np.arange(unique_values[0], unique_values[-1], index_interval)
    
    data_labels = [None] * partitions
    data_values = [None] * partitions
    for i in range(1,len(np_segment_boundaries)):
        
        data_labels[i-1] = f"[{np_segment_boundaries[i-1]}, {np_segment_boundaries[i]})"

        sum = 0
        for value, frequency in zip(unique_values, frequencies):
            if value >= np_segment_boundaries[i-1] and value < np_segment_boundaries[i]:
                sum += frequency
        data_values[i-1] = sum  
    sum = 0
    for value, frequency in zip(unique_values, frequencies):
        if value > np_segment_boundaries[-2] :
            sum += frequency
    data_labels[-1] = f"[{np_segment_boundaries[-2]}, {unique_values[-1]}]"
    data_values[-1] = sum

    return data_labels, data_values