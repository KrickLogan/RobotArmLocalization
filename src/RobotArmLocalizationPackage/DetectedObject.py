import numpy as np
import torch
import numpy.ma as ma
import Utilities.utils as utils

class DetectedObject:

    def __init__(self, box, label, mask, score):
        self.label = label
        self.box = box
        self.mask = mask
        self.score = score
    
    def get_center_pixel(self) -> tuple(int, int):
        x1, y1, x2, y2 = self.box.detach().numpy()
        x = (x1 + x2)/2
        y = (y1 + y2)/2
        return((x,y))

    def get_bool_mask(self):   
        bool_mask = self.mask > utils.PRECISION 
        # assert bool_mask.ndim == 2
        bool_mask = bool_mask.squeeze(1) #########Maybeeee???
        return bool_mask

    def get_average_depth(self, depth_arr) -> float:
        bool_mask = self.get_bool_mask()
        bool_mask = np.logical_and(bool_mask, depth_arr != 0) #discard 0's
        bool_mask = torch.gt(bool_mask, 0) #convert back to boolean
        mx = ma.masked_array(depth_arr, np.invert(bool_mask).long())
        return mx.mean()

    
