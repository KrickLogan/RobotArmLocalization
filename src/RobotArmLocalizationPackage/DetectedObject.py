from matplotlib.pyplot import axis
import numpy as np
from numpy.lib.function_base import average
import torch
import numpy.ma as ma
import Utilities.utils as utils
import sys
class DetectedObject:
    np.set_printoptions(threshold=sys.maxsize)

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

    def get_average_depth(self, depth_arr) -> float:
        bool_mask = self.get_bool_mask()
        bool_mask = np.logical_and(bool_mask, depth_arr != 0)
        print(bool_mask)
        bool_mask = torch.gt(bool_mask, 0) #convert back to boolean
        mx = ma.masked_array(depth_arr, np.invert(bool_mask).long())
        print(mx)
        average_depth = self.remove_depth_outliers(mx)
        return average_depth.mean()
        
    def remove_depth_outliers(self,depth_arr)->np.ndarray:
        #removing outliers
        
        mean= np.mean(depth_arr)
        std= np.std(depth_arr)
        z= [x for x in depth_arr if(x>mean- 3* std)]
        z= [x for x in depth_arr if(x < mean+ 3* std)]
        print(mean,std)
        print(z)
        return z




