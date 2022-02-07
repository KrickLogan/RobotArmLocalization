from matplotlib.pyplot import axis
import numpy as np
from numpy.lib.function_base import average
import torch
import numpy.ma as ma
import Utilities.utils as utils
import sys
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

    def get_average_depth(self, depth_arr) -> float:
        bool_mask = self.get_bool_mask()
        bool_mask = np.logical_and(bool_mask, depth_arr != 0)
        bool_mask =depth_arr != 0
        arr = depth_arr[bool_mask] 
        average_depth = self.remove_depth_outliers(arr)

        return average_depth.mean()  
        
    def remove_depth_outliers(self,depth_arr)->np.ndarray:
        #removing outliers
        mean= np.mean(depth_arr)
        std= np.std(depth_arr)
        print("mean and std is:",mean,std)

        flt = depth_arr.flatten()

        z=flt[(flt>(mean- 3* std)) & (flt<(mean+3* std))]
        print(" Result array : ", z)
        mean = np.mean(z)
        std= np.std(z)
        print(mean,std)
        return z




