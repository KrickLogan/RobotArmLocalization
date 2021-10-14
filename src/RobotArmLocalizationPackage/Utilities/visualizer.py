from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import numpy.ma as ma
import numpy as np
import numpy

def get_rectangles(boxes):
    rectangles = []
    for box in boxes:
        x, y, w, h = box.detach().numpy()
        rectangles.append(Rectangle((x,y), w - x, h - y, edgecolor='red', fill=False))
    return rectangles

def show_mask_overlay(img, mask, title=""):
    plt.imshow(img)
    plt.imshow(mask, cmap='ocean', alpha=.5)
    plt.title(title)
    plt.show()

def show_img_boxes(img, rectangles):
    plt.imshow(img)
    for rect in rectangles:
        plt.gca().add_patch(rect)

    plt.show()



# def show_all_masks(img, masks):
#     bool_masks = get_bool_masks(masks)
#     composite_mask = get_mask_layer(bool_masks)
#     show_img_mask(img, composite_mask)

# def show_mask_with_depth(img, bmask, depth):
#     plt.imshow(img)
#     plt.imshow(bmask.numpy(), cmap='ocean', alpha=.5)
#     plt.title('Depth: ' + str(depth))
#     plt.show()