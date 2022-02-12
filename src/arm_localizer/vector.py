
from __future__ import annotations
import numpy as np
from math import sqrt, acos, degrees, cos, sin
# from arm_localizer.vector import Vector


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

    def __mul__(self, c:float) -> Vector:
        return Vector(c*self.x, c*self.y, c*self.z)

    def __truediv__(self, c) -> Vector:
        return Vector(self.x/c, self.y/c, self.z/c)

    def magnitude(self) -> float :
        mag = sqrt((self.x * self.x + self.y * self.y + self.z * self.z))
        return mag

    def dot(self, other) -> float :
        dot = self.x * other.x + self.y * other.y + self.z * other.z
        return dot

    #def xy_rotate(self, angle):
        #a = np.array([self.x, self.y, self.z])
        #rot = 
        #return 
    
    def rotate_about_vector(self, vNorm:Vector, angle:float) -> Vector:
        '''vNorm must be unit vector'''
        vNorm=vNorm.unit()#just in case
        a = self * cos(angle) 
        b = vNorm.cross(self)*sin(angle) 
        c = vNorm * (vNorm.dot(self)) * (1-cos(angle))
        vrot = a + b + c
        return vrot

    def cross(self, other:Vector) -> Vector:
        i = Vector(1, 0, 0)
        j = Vector(0, 1, 0)
        k = Vector(0, 0, 1)

        cp = i*(self.y*other.z - other.y*self.z) +  j*(self.z*other.x - self.x*other.z) + k*(self.x*other.y - other.x*self.y)

        return cp


    def angle_between(self, other: Vector) -> float:
        
        angle = acos(self.dot(other)/(self.magnitude() * other.magnitude()))
        return angle

    def decompose(self) -> Vector:
        i = Vector(self.x, 0, 0)
        j = Vector(0, self.y, 0)
        k = Vector(0, 0, self.z)
        return i, j, k
    
    def project(self, target: Vector) -> Vector:
        proj = target*(self.dot(target)/(target.magnitude()*target.magnitude()))
        return proj

    def perp(self, u: Vector):
        return self - self.project(u)

    def as_point(self) -> tuple:
        return (self.x, self.y, self.z)
    
    def unit(self):
        return self/self.magnitude()

    def __str__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
        
    def __repr__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
    
