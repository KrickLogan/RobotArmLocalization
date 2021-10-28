import Utilities.utils as utils
from torchvision.transforms import functional as F

class ObjectDetector:

    def __init__(self, img, depth):
        self._img = img
        self._depth = depth
        self._model = utils.load_model()
        self._detections = []
    
    def run(self):
        img_tens = F.to_tensor(self.img)
        output = self._model([img_tens])
        boxes = output[0]['boxes']
        labels = output[0]['labels']
        masks = output[0]['masks']
        scores = output[0]['scores']
        for i in range(len(self.labels)):
            self._detections.append({"label" :  labels[i], "box" : boxes[i],
                "mask" : masks[i], "score" : scores[i]})
        return self._detections
    
    def get_size(self):
        return len(self._detections)
    
    


