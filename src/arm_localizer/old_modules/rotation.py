

class Rotation:
    def __init__(self, f_rot_vector, f_rot_rads, s_rot_vectors, s_rot_rads):
        self._f_rot_vector = f_rot_vector
        self._f_rot_rads= f_rot_rads
        self._s_rot_vector = s_rot_vectors
        self._s_rot_rads = s_rot_rads

    def set_first_rot_vector(self, f_rot_vector):
        self._f_rot_vector=f_rot_vector
    
    def get_first_rot_vector(self):
        return self._f_rot_vector

    def set_first_rot_radian(self, f_rot_rads):
        self._f_rot_rads=f_rot_rads
    
    def get_first_rot_radian(self):
        return self._f_rot_rads
    
    def set_second_rot_vector(self, s_rot_vector):
        self._s_rot_vector=s_rot_vector
    
    def get_second_rot_vector(self):
        return self._s_rot_vector
    
    def set_second_rot_radian(self, s_rot_rads):
        self._s_rot_rads=s_rot_rads
    
    def get_second_rot_radian(self):
        return self._s_rot_rads
