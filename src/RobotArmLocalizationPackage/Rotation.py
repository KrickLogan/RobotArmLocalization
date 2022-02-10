class Rotation:
    def __init__(self, f_rot_vector, f_rot_rads, s_rot_vectors, s_rot_rads):
        #self.val = val
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

    #def __getstate__(self):
        #print("Pickling this value: {self.val}")
        #return self.__dict__
    
    #def __setstate__(self, d):
        #print("Unpickling this value: {self.val}")
        #self.__dict__ = d

#import pickle
#rot = Rotation()
#fh = open ("rotation.pkl", "bw")
#pickle.dump(rot, fh)
#fh.close()
#f = open ("rotation.pkl", "rb")
#f_new = pickle.load(f)
#print(f_new.val)
#f.close()