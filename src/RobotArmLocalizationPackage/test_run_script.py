from PIL import Image
import numpy.ma as ma
import numpy as np
import numpy
import torch
import os
from torchvision.transforms import functional as F
import sys
import Utilities.visualizer as viz
from scipy import ndimage

PRECISION = 0.75

def load_model():
    model = torch.load('model.pt', map_location=torch.device('cpu'))
    return model

def get_bool_masks(masks):   
    bool_masks = masks > PRECISION 
    bool_masks = bool_masks.squeeze(1)
    return bool_masks

def get_composite_masks(bool_masks):
    composite_mask = numpy.zeros((bool_masks[0].size()), bool)
    for mask in bool_masks:
        m = mask.numpy()
        composite_mask = numpy.logical_or(composite_mask, m)
    return composite_mask

def get_avg_depth_of_seg(depth_arr, bool_seg_mask):
    bool_seg_mask = np.logical_and(bool_seg_mask, depth_arr != 0)
    bool_seg_mask = torch.gt(bool_seg_mask, 0)
    mx = ma.masked_array(depth_arr, np.invert(bool_seg_mask).long())
    return mx.mean()

def center_of_mask(mask):
    return ndimage.measurements.center_of_mass(mask)

def get_center(boxes):
    points = []
    for box in boxes:
        x, y, w, h = box.detach().numpy()
        p1 = (w + x)/2
        p2 = (h + y)/2
        points += [p1, p2]
    return points

# def size_img_tensor(tens):
#     if tens.size()[0] > 3:
#         tens = tens[0:3]
#     return tens

def main(img_name):

        img = Image.open(os.path.join("Data/Images/",img_name + ".png")).convert("RGB")
        # img = Image.open(os.path.join("Data/Images/",img_name + ".png"))
        np_depth = np.load(f"Data/Depths/{img_name}_depth.npy")
        model = load_model()
        img_tens = F.to_tensor(img)
        # img_tens = size_img_tensor(img_tens)
        output = model([img_tens])
        
        boxes = output[0]['boxes']
        labels = output[0]['labels']
        masks = output[0]['masks']
        scores = output[0]['scores']

        viz.show_img(img)

        # rectangles = viz.get_rectangles(boxes)
        # viz.show_img_boxes(img, rectangles)

        bool_masks = get_bool_masks(masks)
        # viz.show_mask_overlay(img, get_composite_masks(bool_masks), "All Mask Predictions")
        
        avg_depths = []
        mask_depths = []
        
        for bmask in bool_masks: 
            avg_depths.append(get_avg_depth_of_seg(np_depth, bmask))
            mask_depths.append(ma.masked_array(np_depth, np.invert(bmask).long()))
        
        print(f'Labels: {labels}')
        print(f'Scores: {scores}')
        print(f'Avg Depths: {avg_depths}')

        for i in range(len(masks)):
            # data_labels, data_values = viz.get_graph_labels_values(mask_depths[i])
            # viz.show_bar_graph(data_labels, data_values, f"Depth Spread {viz.get_label_string(labels[i])}\nAVG Depth: {avg_depths[i]}", "Range", "Frequency")
            # viz.show_mask_overlay(np_depth, bool_masks[i], "Mask Over Depth", True, np_depth)
            plt_title = f'Label: {viz.get_label_string(labels[i])}, Score: {round(scores[i].item(),4)}, Average Depth: {round(avg_depths[i], 4)}'
            # viz.show_mask_overlay(img, bool_masks[i], plt_title, True, np_depth)
            viz.show_mask_overlay(img, bool_masks[i], plt_title)
            # print(np.unique(bool_masks[i].numpy().astype(int)))
            # mask_center = center_of_mask(bool_masks[i].numpy().astype(int))
            
            # viz.show_point(img, mask_center, "mask and center", bool_masks[i])
            
        
        viz.show_img_mask_center_point(img, boxes, get_center(boxes))


if __name__ == "__main__":
    main(sys.argv[1])
    