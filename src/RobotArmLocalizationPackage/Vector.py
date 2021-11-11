'''
    Note that all of the coordinate values are such that x is horizontal,
    y is DEPTH, and z is vertical in 3d space relative to the camera.
'''
import numpy as np
from math import cos, sin

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    

    def __add__(self, other):
        a = np.array([self.x, self.y, self.z])
        b = np.array([other.x, other.y, other.z])
        return a + b

    def __sub__(self, other):
        a = np.array([self.x, self.y, self.z])
        b = np.array([other.x, other.y, other.z])
        return a - b

    def magnitude(self):
        a = np.array([self.x, self.y, self.z])
        mag = np.sqrt(a.dot(a))
        return mag

    def dot(self, other):
        a = np.array([self.x, self.y, self.z])
        b = np.array([other.x, other.y, other.z])
        return np.dot(a, b)

   # def xy_rotate(self, angle):
        #a = np.array([self.x, self.y, self.z])
        #rot = 
        #return 

    def angle_between(self, other):
        a = np.array([self.x, self.y, self.z])
        b = np.array([other.x, other.y, other.z])
        dot = np.dot(a, b)
        return np.arccos(dot)

    def __str__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
    def __repr__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")