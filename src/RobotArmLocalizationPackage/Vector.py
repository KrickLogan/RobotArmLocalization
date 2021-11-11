'''
    Note that all of the coordinate values are such that x is horizontal,
    y is DEPTH, and z is vertical in 3d space relative to the camera.
'''
import numpy as np
from math import cos, sin, sqrt
from Vector import Vector

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other) -> Vector :
        newx = self.x + other.x
        newy = self.y + other.y
        newz = self.z + other.z
        return Vector(newx, newy, newz)

    def __sub__(self, other) -> Vector :
        newx = self.x - other.x
        newy = self.y - other.y
        newz = self.z - other.z
        return Vector(newx, newy, newz)

    def magnitude(self) -> float :
        mag = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return mag

    def dot(self, other) -> float :
        dot = self.x * other.x + self.y * other.y + self.z * other.z
        return dot

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