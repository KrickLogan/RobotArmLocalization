import os
import numpy as np
from PIL import Image
from Utilities.custom_utils import get_image_fnames, remove_unmatched_fnames, remove_unwanted_files
import Utilities.custom_utils as cu

mask_fnames = list(sorted(os.listdir("Data/PNGMasks")))

mask_fnames = cu.remove_bad_mask_files(mask_fnames)

image_fnames = get_image_fnames(mask_fnames)

image_fnames = cu.remove_bad_img_files(image_fnames)

all_image_fnames = list(sorted(os.listdir("Data/PNGImages")))

image_fnames, mask_fnames = remove_unmatched_fnames(image_fnames, mask_fnames, all_image_fnames)

np_masks = []
np_imgs = []
rework_masks = []
rework_masks_colors = []
correct_unique_values = [0,64,127,255]

# image_fnames = remove_unwanted_files(image_fnames)
# mask_fnames = remove_unwanted_files(mask_fnames)

for img in image_fnames:
    np_imgs.append((np.array(Image.open(os.path.join("Data/PNGImages",img))), img))

for mask in mask_fnames:
    np_masks.append((np.array(Image.open(os.path.join("Data/PNGMasks", mask))), mask))

for mask_d,img_d in zip(np_masks, np_imgs):
    # print(mask.shape)
    mask = mask_d[0]
    img = img_d[0]
    mask_name = mask_d[1]
    img_name = img_d[1]

    print(f'\nMask: {mask_name}')
    dimension = mask.shape == img.shape[:-1]
    num_unique_values = len(np.unique(mask))
    print(f"mask shape = {mask.shape}, img shape = {img.shape} dimension equivalent: {dimension}")
    print(f"unique values mask data: {np.unique(mask)} {num_unique_values == 4}")
    
    # Check for incorrect dimension (grayscale/alpha channel check)
    if not dimension:
        print(f'!!! Rework Required: {mask_name}')
        rework_masks.append(mask_name)

    # Check for incorrect colors or number of unique values
    if not np.array_equal(np.unique(mask), correct_unique_values) or num_unique_values != 4:
        print(f'!!! Rework Required: {mask_name}')
        rework_masks_colors.append(mask_name)

# Display arrays of the masks that require rework
print('\n--------------------------------------------------------------------------------------')
print('\nThe following masks require rework:')
print('\nRemove alpha channel or set to grayscale in the following masks:')
print(rework_masks)
print('\nIncorrect number of unique values or incorrect colors are used in the following masks:')
print(rework_masks_colors)
