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

def remove_unwanted_files(fnames):
    substring = 'frame'
    for fname in fnames:
        if substring not in fname:
            fnames.remove(fname)
    return fnames
