'''
    Note that all of the coordinate values are such that x is horizontal,
    y is DEPTH, and z is vertical in 3d space relative to the camera.
'''
import numpy as np
from math import sqrt, acos, degrees, cos, sin
import Vector

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
        a = self * cos(angle) 
        b = vNorm.cross(self)*sin(angle) 
        c = vNorm * (vNorm.dot(self)) * (1-cos(angle))
        vrot = a + b + c
        print(f"a: {a}, b: {b}, c: {c}")
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

    # def get_signed_angles(self, other: Vector) -> float:

    #     self_xy_proj = Vector(self.x, self.y, 0)
    #     self_yz_proj = Vector(0, self.y, self.z)
    #     self_xz_proj = Vector(self.x, 0, self.z)

    #     other_xy_proj = Vector(other.x, other.y, 0)
    #     other_yz_proj = Vector(0, other.y, other.z)
    #     other_xz_proj = Vector(other.x, 0, other.z)


    #     i = Vector(1, 0, 0)
    #     j = Vector(0, 1, 0)
    #     k = Vector(0, 0, 1)

    #     xy_plane_angle = i.angle_between(other_xy_proj) - i.angle_between(self_xy_proj)
    #     yz_plane_angle = j.angle_between(other_yz_proj) - j.angle_between(self_yz_proj)
    #     xz_plane_angle = k.angle_between(other_xz_proj) - k.angle_between(self_xz_proj)

    #     return xy_plane_angle, yz_plane_angle, xz_plane_angle



    def decompose(self) -> Vector:
        i = Vector(self.x, 0, 0)
        j = Vector(0, self.y, 0)
        k = Vector(0, 0, self.z)
        return i, j, k
    

    def __str__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
        
    def __repr__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")