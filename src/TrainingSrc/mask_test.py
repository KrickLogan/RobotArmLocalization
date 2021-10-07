import os
import numpy as np
from PIL import Image

masks = list(sorted(os.listdir("Data/PNGMasks")))
images = list(sorted(os.listdir("Data/PNGImages")))
np_masks = []
np_imgs = []
correct_unique_values = [0,64,127,255]
rework_masks = []
rework_masks_colors = []

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
    print(f"unique values mask data: {np.unique(mask)} {num_unique_values == 4}")
    
    # Check for incorrect dimension or number of unique values
    if not dimension or num_unique_values != 4:
        print(f'!!! Rework Required: {mask_name}')
        rework_masks.append(mask_name)

    # Check for incorrect colors
    if not np.array_equal(np.unique(mask), correct_unique_values):
        print(f'!!! Rework Required: {mask_name}')
        rework_masks_colors.append(mask_name)

# Display arrays of the masks that require rework
print('\n--------------------------------------------------------------------------------------')
print('\nThe following masks require rework:')
print('\nRemove alpha channel or set to grayscale in the following masks:')
print(rework_masks)
print('\nIncorrect colors are used in the following masks:')
print(rework_masks_colors)
