
from typing import List
import torch
import Utilities.utils as utils
from torchvision.transforms import functional as F
from DetectedObject import DetectedObject
from PIL import Image
from inspect import currentframe, getframeinfo

class ObjectDetector:

    def __init__(self, img):
        self._img = img
        self._model = torch.load('model.pt', map_location=torch.device('cpu'))
        self._output = None
        self.claw = DetectedObject
        self.base = DetectedObject
        self.object = DetectedObject
    
    def run(self) -> List[DetectedObject]:
        # runs the model on the provided image
        img_tens = F.to_tensor(self._img)
        self._output = self._model([img_tens])
        boxes = self._output[0]['boxes']
        labels = self._output[0]['labels']
        masks = self._output[0]['masks']
        scores = self._output[0]['scores']
        for i in range(len(boxes)):
            label, box, mask, score = labels[i],boxes[i], masks[i], scores[i]
            label_string = utils.get_label_string(label)
            if label_string == utils.BASE_STRING:
                self.base = DetectedObject(label_string, box, mask, score)
            elif label_string == utils.CLAW_STRING:
                self.claw = DetectedObject(label_string, box, mask, score)
            elif label_string == utils.COTTON_STRING:
                self.object = DetectedObject(label_string, box, mask, score)
            else:
                utils.fail(getframeinfo(currentframe()))
            # self._detections.append(obj)
        return self._output #Do something if more than one or none are detected for any of the target labels
    
    def get_model_outputs(self):
        return self._output

    # def get_size(self):
    #     return len(self._detections)
    
    def get_image_size(self):
        return self._img.size
    
    def get_claw(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        return self.claw
        
    def get_base(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        return self.base

    def get_object(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        return self.object

