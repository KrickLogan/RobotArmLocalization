
from typing import List

from torchvision.transforms import functional as F
from .detected_object import DetectedObject
from .utilities import utils
# import utilities.utils as utils
from PIL import Image
from inspect import currentframe, getframeinfo

class ObjectDetector:
    """This class uses the trained RCNN to make detections on an image. It handles the output of the model.

    This class provides an interface for the detections yielded from the model. It can provide the full output
    from the model, or processed individual detections from the model in the form of :class:`arm_localizer.detected_object.DetectedObject` 's

    Attributes:
        _img (PIL.Image): Will be changed
        _model (): The trained model
        _output (): the output of the model as a multi-dimensional array
        claw : won't be here much longer
        base: same
        object: same
    """
    def __init__(self, img):
        """Constructor method
        """
        # self._img = img
        self._model = utils.load_model()
        self._output = None
        self._detections = None
        # self.claw = DetectedObject
        # self.base = DetectedObject
        # self.object = DetectedObject
    
    # def __init__(self):
    #     self._model = torch.load('model.pt', map_location=torch.device('cpu'))
    #     self._output = None

    def run(self, img) -> List[DetectedObject]:
        # runs the model on the provided image
        """Runs the model on the provided image

        This method runs the model on the image. It then interprets and organizes the output
        by classifying detections and constructing new :class:`arm_localizer.detected_object.DetectedObject`'s
        for each detection.

        Args:
            None right now but will change in next version

        Returns:
            detections: the model detections. changed in next version

        """
        img_tens = F.to_tensor(self._img)
        self._output = self._model([img_tens])
        boxes = self._output[0]['boxes']
        labels = self._output[0]['labels']
        masks = self._output[0]['masks']
        scores = self._output[0]['scores']
        for i in range(len(boxes)):
            label, box, mask, score = labels[i],boxes[i], masks[i], scores[i]
            label_string = utils.get_label_string(label)
            
            obj = DetectedObject(label_string, box, mask, score)
            self._detections.append(obj)
            # if label_string == utils.BASE_STRING:
            #     base = DetectedObject(label_string, box, mask, score)
            # elif label_string == utils.CLAW_STRING:
            #     claw = DetectedObject(label_string, box, mask, score)
            # elif label_string == utils.COTTON_STRING:
            #     object = DetectedObject(label_string, box, mask, score)
            # else:
            #     utils.fail(getframeinfo(currentframe()))
            # self._detections.append()
        return self._detections #Do something if more than one or none are detected for any of the target labels
    
    def get_model_outputs(self):
        """I think this will be gone soon too

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        return self._output

    def get_all_detections(self):
        return self._detections

    # def get_size(self):
    #     return len(self._detections)
    
    def get_image_size(self):
        """I think this will be gone soon too

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        return self._img.size
    
    def get_claw(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        for obj in self._detections:
            if obj.get_label() == utils.CLAW_STRING:
                return obj
        return False
        
    def get_base(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        for obj in self._detections:
            if obj.get_label() == utils.BASE_STRING:
                return obj
        return False

    def get_object(self) -> DetectedObject: # shouldn't return a list, error check at detection level to allow 1 and only 1 of each "type " ie claw, boject, base
        for obj in self._detections:
            if obj.get_label() == utils.COTTON_STRING:
                return obj
        return False
    
