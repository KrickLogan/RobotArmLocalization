import os
import numpy as np
from PIL import Image

masks = list(sorted(os.listdir("Data/PNGMasks")))
images = list(sorted(os.listdir("Data/PNGImages")))
np_masks=[]
np_imgs = []

for img in images:

    np_imgs.append((np.array(Image.open(os.path.join("Data/PNGImages",img))), img))
for mask in masks:
    np_masks.append((np.array(Image.open(os.path.join("Data/PNGMasks", mask))), mask))

for mask_d,img_d in zip(np_masks, np_imgs):
    # print(mask.shape)
    mask = mask_d[0]
    img = img_d[0]
    mask_name = mask_d[1]
    img_name = img_d[1]

    print('')
    print(f'Mask: {mask_name}')
    dimension = mask.shape == img.shape[:-1]
    num_unique_values = len(np.unique(mask))
    print(f"mask shape = {mask.shape}, img shape = {img.shape} dimension equivalent: {dimension}")
    print(f"unique values mask data: {np.unique(mask)} {num_unique_values == 3}")
    
    if not dimension or num_unique_values != 3:
        print(mask_name)