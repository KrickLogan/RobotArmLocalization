from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import numpy.ma as ma
import numpy as np
import torch
import sys

from torchvision.transforms import functional as F

def load_model():
    model = torch.load('model.pt', map_location=torch.device('cpu'))
    return model

def get_rectangles(boxes):
    rectangles = []
    for box in boxes:
        x, y, w, h = box.detach().numpy()
        rectangles.append(Rectangle((x,y), w - x, h - y, edgecolor='red', fill=False))
    return rectangles
        
def get_mask_layer(masks):
    bool_masks = masks > .5
    bool_masks = bool_masks.squeeze(1)
    composite_mask = numpy.zeros((masks[0].size), bool)
    for mask in bool_masks:
        m = mask.numpy()
        composite_mask = np.logical_or(composite_mask, m)
    return composite_mask
    

def show_img_mask(img, mask):
    
    plt.imshow(img)
    plt.imshow(mask)
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

def main(file_name):
    model = load_model()
    img = get_img(file_name)
    img_tens = F.to_tensor(img)
    output = model([img_tens])
    boxes = output[0]['boxes']
    labels = output[0]['labels']
    masks = output[0]['masks']
    show_masks(masks[0])
    scores = output[0]['scores']
    print(boxes)
    rectangles = get_rectangles(boxes)
    show_img(img, rectangles)
    


if __name__ == "__main__":
    file_name = sys.argv[1]
    main(file_name)