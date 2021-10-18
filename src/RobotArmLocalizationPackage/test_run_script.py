from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
from PIL import Image
import numpy.ma as ma
import numpy as np
import numpy
import torch
import os
from torchvision.transforms import functional as F
import sys
import Utilities.visualizer as viz

PRECISION = 0.75

# depths = list(sorted(os.listdir("src/RobotArmLocalizationPackage/Data/Depths")))
# images = list(sorted(os.listdir("src/RobotArmLocalizationPackage/Data/Images")))
# np_depths = []
# np_imgs = []

# for depth in depths:
#     if not os.path.basename(depth) == '.gitkeep':
#         np_depths.append(np.array(np.load(os.path.join("src/RobotArmLocalizationPackage/Data/Depths/", depth))))

# for img in images:
#     if not os.path.basename(img) == '.gitkeep':
#         np_imgs.append(Image.open(os.path.join("src/RobotArmLocalizationPackage/Data/Images/",img)))

def load_model():
    model = torch.load('model.pt', map_location=torch.device('cpu'))
    return model

def get_rectangles(boxes):
    rectangles = []
    for box in boxes:
        x, y, w, h = box.detach().numpy()
        rectangles.append(Rectangle((x,y), w - x, h - y, edgecolor='red', fill=False))
    return rectangles

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
    plt.imshow(img)
    plt.title('Original Image')
    # maximize_plt()
    plt.show()

def show_img_mask(img, mask):
    plt.imshow(img)
    plt.imshow(mask, cmap='ocean', alpha=.5)
    plt.title('Predicted Masks')
    # maximize_plt()
    plt.show()

def show_all_masks(img, masks):
    bool_masks = get_bool_masks(masks)
    composite_mask = get_mask_layer(bool_masks)
    show_img_mask(img, composite_mask)

def show_mask_with_depth(img, bmask, depth):
    plt.imshow(img)
    plt.imshow(bmask.numpy(), cmap='ocean', alpha=.25)
    plt.title('Depth: ' + str(depth))
    plt.show()

def show_mask_with_score_label(img, bmask, score, label):
    plt.imshow(img)
    plt.imshow(bmask.numpy(), cmap='ocean', alpha=.5)
    plt.title(f'Label: {get_label_string(label)}, Score: {round(score.item(),4)}')
    maximize_plt()
    plt.show()

def show_mask_with_score_label_depth(img, bmask, score, label, depth, depth_arr):
    plt.imshow(img)
    plt.imshow(bmask.numpy(), cmap='ocean', alpha=.5)
    plt.imshow(depth_arr, alpha=0)
    plt.title(f'Label: {get_label_string(label)}, Score: {round(score.item(),4)}, Average Depth: {round(depth, 4)}')
    maximize_plt()
    plt.show()

def show_img_boxes(img, rectangles):
    plt.imshow(img)
    plt.title('Predicted Bounding Boxes')
    for rect in rectangles:
        plt.gca().add_patch(rect)

    maximize_plt()
    plt.show()

def get_avg_depth_of_seg(depth_arr, bool_seg_mask):
    bool_seg_mask = np.logical_and(bool_seg_mask, depth_arr != 0)
    bool_seg_mask = torch.gt(bool_seg_mask, 0)
    mx = ma.masked_array(depth_arr, np.invert(bool_seg_mask).long())
    return mx.mean()

def size_img_tensor(tens):
    if tens.size()[0] > 3:
        tens = tens[0:3]
    return tens

def maximize_plt():
    # if OS is Windows the plot will be maximized :)
    if os.name == 'nt':
        mng = plt.get_current_fig_manager() 
        mng.window.state("zoomed")

# def main():
#     for i in range(len(np_imgs)):
#         img = np_imgs[i]
#         depth_arr = np_depths[i]

#         model = load_model()
#         img_tens = F.to_tensor(img)
#         img_tens = size_img_tensor(img_tens)
#         output = model([img_tens])
        
#         boxes = output[0]['boxes']
#         labels = output[0]['labels']
#         masks = output[0]['masks']
#         scores = output[0]['scores']

#         show_img(img)

#         rectangles = get_rectangles(boxes)
#         show_img_boxes(img, rectangles)

#         show_all_masks(img, masks)

#         avg_depths = []
#         bool_masks = get_bool_masks(masks)
#         for bmask in bool_masks: 
#             avg_depths.append(get_avg_depth_of_seg(depth_arr, bmask))

#         print(f'Labels: {labels}')
#         print(f'Scores: {scores}')
#         print(f'Avg Depths: {avg_depths}')

#         for i in range(len(masks)):
#             #if scores[i] >= 0.90:
#             show_mask_with_score_label_depth(img, bool_masks[i], scores[i], labels[i], avg_depths[i], depth_arr)

def main(img_name):

        img = Image.open(os.path.join("Data/Images/",img_name + ".png"))
        np_depth = np.load(f"Data/Depths/{img_name}_depth.npy")
        model = load_model()
        img_tens = F.to_tensor(img)
        img_tens = size_img_tensor(img_tens)
        output = model([img_tens])
        
        boxes = output[0]['boxes']
        labels = output[0]['labels']
        masks = output[0]['masks']
        scores = output[0]['scores']

        show_img(img)

        # rectangles = get_rectangles(boxes)
        # show_img_boxes(img, rectangles)

        # show_all_masks(img, masks)
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
            data_labels, data_values = viz.get_graph_labels_values(mask_depths[i])
            viz.show_mask_overlay(np_depth, bool_masks[i], "Mask Over Depth", True, np_depth)
            viz.show_bar_graph(data_labels, data_values, f"Depth Spread {get_label_string(labels[i])}\nAVG Depth: {avg_depths[i]}", "Range", "Frequency")
            
        # for i in range(len(masks)):
            #if scores[i] >= 0.90:
            # show_mask_with_score_label_depth(img, bool_masks[i], scores[i], labels[i], avg_depths[i], depth_arr)


if __name__ == "__main__":
    main(sys.argv[1])
    