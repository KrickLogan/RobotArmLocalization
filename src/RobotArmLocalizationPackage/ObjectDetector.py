
from typing import List
import Utilities.utils as utils
from torchvision.transforms import functional as F
from DetectedObject import DetectedObject
from PIL import Image

class ObjectDetector:

    def __init__(self, img : Image):
        self._img = img
        self._model = utils.load_model()
        self._detections = []
    
    def run(self) -> List[DetectedObject]:
        img_tens = F.to_tensor(self.img)
        output = self._model([img_tens])
        boxes = output[0]['boxes']
        labels = output[0]['labels']
        masks = output[0]['masks']
        scores = output[0]['scores']
        for i in range(len(self.labels)):
            label, box, mask, score = labels[i],boxes[i], masks[i], scores[i]
            self._detections.append(DetectedObject(label, box, mask, score))
        return self._detections #Do something if more than one or none are detected for any of the target labels
    
    def get_size(self):
        return len(self._detections)
    
    def get_detections(self) -> List[DetectedObject]:
        return self._detections
    
    def get_claw(self) -> List[DetectedObject]:
        return any(el.label == utils.CLAW_STRING for el in self._detections)
    
    def get_base(self) -> List[DetectedObject]:
        return any(el.label == utils.BASE_STRING for el in self._detections)
    
    def get_object(self) -> List[DetectedObject]:
        return any(el.label == utils.COTTON_STRING for el in self._detections)


