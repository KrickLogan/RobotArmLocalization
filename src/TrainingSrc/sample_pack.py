from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import numpy.ma as ma
import numpy as np
import numpy
import torch
import sys

from torchvision.transforms import functional as F

PRECISION = .5

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

def get_mask_layer(bool_masks):

    composite_mask = numpy.zeros((bool_masks[0].size()), bool)
    for mask in bool_masks:
        print(mask.size())
        m = mask.numpy()
        composite_mask = numpy.logical_or(composite_mask, m)
    return composite_mask
    

def show_img_mask(img, mask):
    plt.imshow(img)
    plt.imshow(mask, cmap='ocean', alpha=.5)
    plt.show()

def show_all_masks(img, masks):
    bool_masks = get_bool_masks(masks)
    composite_mask = get_mask_layer(bool_masks)
    show_img_mask(img, composite_mask)

def show_mask_with_depth(img, bmask, depth):
    
    plt.imshow(img)
    plt.imshow(bmask.numpy(), cmap='ocean', alpha=.5)
    plt.title('Depth: ' + str(depth))
    plt.show()


def get_img(fname):
    img_path = 'PennFudanPed/PNGImages/' + fname
    img = mpimg.imread(img_path)
    return img

def show_img_boxes(img, rectangles):
    
    plt.imshow(img)
    for rect in rectangles:
        plt.gca().add_patch(rect)

    plt.show()

def get_depth_of_seg(depth_arr, bool_seg_mask):
    mx = ma.masked_array(depth_arr, np.invert(bool_seg_mask).long())
    print(mx)
    return mx.mean()

def get_rand_depth_array(size):
    return numpy.random.randint(0, 500, size) 

def size_img_tensor(tens):
    if tens.size()[0] > 3:
        tens = tens[0:3]
    return tens

def main(file_name):
    
    
    model = load_model()
    img = get_img(file_name)
    img_tens = F.to_tensor(img)
    img_tens = size_img_tensor(img_tens)
    output = model([img_tens])
    
    boxes = output[0]['boxes']
    labels = output[0]['labels']
    masks = output[0]['masks']
    scores = output[0]['scores']

    rectangles = get_rectangles(boxes)
    show_img_boxes(img, rectangles)

    show_all_masks(img, masks)

    size = img_tens[0].size()
    depth_arr = get_rand_depth_array(size)
    avg_depths = []
    bool_masks = get_bool_masks(masks)
    for bmask in bool_masks: 
        avg_depths.append(get_depth_of_seg(depth_arr, bmask))

    
    for bmask, depth in zip(bool_masks, avg_depths):
        show_mask_with_depth(img, bmask, depth) 


if __name__ == "__main__":
    file_name = sys.argv[1]
    main(file_name)