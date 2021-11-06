import os
import re

from PIL import Image
import numpy as np

def get_image_fnames(mask_fnames):
        image_fnames = [mask.replace('_mask', '') for mask in mask_fnames]
        return image_fnames

def remove_unmatched_fnames(image_fnames, mask_fnames, all_image_fnames):
    missing_images = list(set(image_fnames).difference(set(all_image_fnames)))
    if len(missing_images)>0 :
        print('File Name Error: files removed')
        print(f'Missing PNGImages: {missing_images}')
        for m_image in missing_images:
            image_fnames.remove(m_image)
            mask_fnames.remove(m_image.replace('.', '_mask.'))
    return image_fnames, mask_fnames

# def remove_unwanted_files(fnames):
#     substring = 'frame'
#     for fname in fnames:
#         if substring not in fname:
#             fnames.remove(fname)
#     return fnames

def remove_bad_img_files(fnames):
    good_img_files = []
    for fname in fnames:
        if bool(re.match("frame_\d{1,3}\\.png", fname)):
            good_img_files.append(fname)
    return good_img_files

def remove_bad_mask_files(mfnames):
    good_mask_files = []
    for fname in mfnames:
        if bool(re.match("frame_\d{1,3}_mask\\.png", fname)):
            good_mask_files.append(fname)
        
    return good_mask_files

def exclude_incorrect_masks(mask_fnames):
    np_masks = []
    correct_mask_fnames = []

    for mask_i in mask_fnames:
        np_masks.append((np.array(Image.open(os.path.join("Data/PNGMasks", mask_i)).convert('L')), mask_i))

    for mask_d in np_masks:

        mask = mask_d[0]
        mask_name = mask_d[1]
    
        num_unique_values = len(np.unique(mask))

        if num_unique_values == 4:
            correct_mask_fnames.append(mask_name)
        else:
            print(f'Excluding Incorrect Mask: {mask_name}')

    if correct_mask_fnames != []:
        print(f'\nNOTICE:\n Please run "mask_test.py" for more information on incorrect masks!\n')
            
    return correct_mask_fnames