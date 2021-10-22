from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import numpy.ma as ma
import numpy as np


def get_rectangles(boxes):
    rectangles = []
    for box in boxes:
        x, y, w, h = box.detach().numpy()
        rectangles.append(Rectangle((x,y), w - x, h - y, edgecolor='red', fill=False))
    return rectangles


def show_mask_overlay(img, mask, title="", force_contrast=False, depth_arr=None):
    if force_contrast: 
        plt.imshow(img, vmin=350, vmax = 614)
    else:
        plt.imshow(img)
    plt.imshow(mask, cmap='ocean', alpha=.5)
    if depth_arr is not None:
        plt.imshow(depth_arr, alpha=0)
    plt.title(title)
    plt.show()

def show_img_boxes(img, rectangles):
    plt.imshow(img)
    for rect in rectangles:
        plt.gca().add_patch(rect)

    plt.show()

def show_bar_graph(data_labels, data_values, title="", x_axis_label="", y_axis_label=""):
    label_indices = [i for i, _ in enumerate(data_labels)]
    plt.bar(label_indices, data_values, color="blue")
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.title(title)
    plt.xticks(label_indices, data_labels)
    plt.show()

def get_graph_labels_values(ma_depth):
    partitions = 6
    unique_values, frequencies = np.unique(ma_depth, return_counts=True)
    
    for i in range(len(unique_values)):   
        if not np.isscalar(unique_values[i]):
            frequencies = np.delete(frequencies, i)
            unique_values = np.delete(unique_values, i)

    print(f"Percentage 0: {frequencies[0]/frequencies[1:].sum()} ")
    
    frequencies = frequencies[1:]
    unique_values = unique_values[1:]
    
    index_interval = (unique_values[-1] - unique_values[0])//(partitions)
    
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

    

# def show_all_masks(img, masks):
#     bool_masks = get_bool_masks(masks)
#     composite_mask = get_mask_layer(bool_masks)
#     show_img_mask(img, composite_mask)

# def show_mask_with_depth(img, bmask, depth):
#     plt.imshow(img)
#     plt.imshow(bmask.numpy(), cmap='ocean', alpha=.5)
#     plt.title('Depth: ' + str(depth))
#     plt.show()