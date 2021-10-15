import os
import numpy as np
from PIL import Image
import pytest

def get_image_fnames(mask_fnames):
    image_fnames = [mask.replace('_mask', '') for mask in mask_fnames]
    return image_fnames

def remove_unmatched_fnames(image_fnames, mask_fnames, all_image_fnames):
    missing_images = list(set(image_fnames).difference(set(all_image_fnames)))
    if len(missing_images)>0 :
        print('File Name Error: files removed')
        print(missing_images)
        for m_image in missing_images:
            image_fnames.remove(m_image)
            mask_fnames.remove(m_image.replace('.', '_mask.'))
    return image_fnames, mask_fnames

mask_fnames = list(sorted(os.listdir("Data/PNGMasks")))
image_fnames = get_image_fnames(mask_fnames)
all_image_fnames = list(sorted(os.listdir("Data/PNGImages")))
image_fnames, mask_fnames = remove_unmatched_fnames(image_fnames, mask_fnames, all_image_fnames)

np_masks = []
np_imgs = []
rework_masks = []
rework_masks_colors = []
correct_unique_values = [0,64,127,255]

for img in image_fnames:
    if not os.path.basename(img) == '.gitkeep' and not os.path.basename(img) == '.DS_Store':
        np_imgs.append((np.array(Image.open(os.path.join("Data/PNGImages",img))), img))

for mask in mask_fnames:
    if not os.path.basename(mask) == '.gitkeep' and not os.path.basename(mask) == '.DS_Store':
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
