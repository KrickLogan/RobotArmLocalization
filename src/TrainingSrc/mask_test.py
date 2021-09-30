import os
import numpy as np
from PIL import Image

masks = list(sorted(os.listdir("Data/PNGMasks")))
images = list(sorted(os.listdir("Data/PNGImages")))
np_masks=[]
np_imgs = []
for img in images:

    np_imgs.append(np.array(Image.open(os.path.join("Data/PNGImages",img))))
for mask in masks:
    np_masks.append(np.array(Image.open(os.path.join("Data/PNGMasks", mask))))

for mask,img in zip(np_masks, np_imgs):
    # print(mask.shape)
    print(f"mask shape = {mask.shape}, img shape = {img.shape} {mask.shape == img.shape[:-1]}")
