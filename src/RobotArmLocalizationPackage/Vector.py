'''
    Note that all of the coordinate values are such that x is horizontal,
    y is DEPTH, and z is vertical in 3d space relative to the camera.
'''

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    

    # def __add__(self, other)
    # def __sub__(self, other)
    # def magnitude(self)
    # def dot(self, other)
    # def xy_rotate(self, angle)
    # def angle_between(self, other)

    def __str__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")
    def __repr__(self) -> str:
        return(f"({self.x}, {self.y}, {self.z})")