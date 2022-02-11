from matplotlib.pyplot import axis
import numpy as np
from numpy.lib.function_base import average
import torch
import numpy.ma as ma
import Utilities.utils as utils

class DetectedObject:
    def __init__(self, label, box, mask, score):
        self.label = label
        self.box = box
        self.mask = mask
        self.score = score
    
    def get_center_pixel(self) -> tuple:
        x1, y1, x2, y2 = self.box.detach().numpy()
        x = (x1 + x2)/2
        y = (y1 + y2)/2
        return((x,y))

    def get_label(self):
        return self.label

    def get_bool_mask(self) -> np.ndarray:   
        bool_mask = self.mask > utils.PRECISION
        # assert bool_mask.ndim == 2
        bool_mask = np.squeeze(bool_mask)
        return bool_mask

    def get_masked_array(self, depth_arr)->np.ma:
        bool_mask = self.get_bool_mask()
        bool_mask = np.logical_and(bool_mask, depth_arr != 0)
        bool_mask = torch.gt(bool_mask, 0) #convert back to boolean
        mx = ma.masked_array(depth_arr, np.invert(bool_mask).long()) 
        return(mx)

    def get_average_depth(self, masked_depth_arr) -> float:
        mx = self.get_masked_array(masked_depth_arr)
        average_depth = self.remove_depth_outliers(mx)

        return np.ma.MaskedArray.mean(average_depth)
        
    def remove_depth_outliers(self,masked_depth_arr) -> np.ma:
        #removing outliers
        mean= np.ma.MaskedArray.mean(masked_depth_arr)
        std= np.ma.MaskedArray.std(masked_depth_arr)
        print("mean and std is:",mean,std)

        z = masked_depth_arr [(masked_depth_arr>(mean- 3* std)) & (masked_depth_arr<(mean+3* std))]

        # print(" Result array : ", z)
        # mean = np.ma.MaskedArray.mean(z)
        # std= np.ma.MaskedArray.mean(z)
        # print("mean,std after removing high values:",mean,std)
        return z
