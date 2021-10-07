# Sample code from the TorchVision 0.3 Object Detection Finetuning Tutorial
# http://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

import os
import numpy as np
import torch
from PIL import Image

import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

from engine import train_one_epoch, evaluate
import utils
import transforms as T

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

def show(img, title="title"):
    plt.title(title)
    plt.imshow(img)
    plt.show()

class ClawObjectDataset(object):
    def __init__(self, root, transforms):
        self.root = root
        self.transforms = transforms
        # load all image files, sorting them to
        # ensure that they are aligned
        self.imgs = list(sorted(os.listdir(os.path.join(root, "PNGImages"))))
        self.masks = list(sorted(os.listdir(os.path.join(root, "PNGMasks"))))
        # print(1)
        # print(self.masks)

    def __getitem__(self, idx):
        # load images and masks
        img_path = os.path.join(self.root, "PNGImages", self.imgs[idx])
        mask_path = os.path.join(self.root, "PNGMasks", self.masks[idx])
        
        # print(img_path)
        # print(mask_path)

        # for i in range(len(self.imgs)):
        #     print(f"{self.imgs[i]},{self.masks[i]}")
        img = Image.open(img_path).convert("RGB")
        # note that we haven't converted the mask to RGB,
        # because each color corresponds to a different instance
        # with 0 being background
        mask = Image.open(mask_path)

        mask = np.array(mask)
        
        # show(mask, mask_path)

        # instances are encoded as different colors
        obj_ids = np.unique(mask)

        # print(mask.shape)
        for i in range(len(obj_ids)):
            mask = np.where(mask == obj_ids[i], i, mask)
        
        for i in range(len(obj_ids)):
            obj_ids[i] = i
        # print(mask.shape)

        # show(mask)
        # print("np.unique(mask)")
        # print(np.unique(mask))

        # first id is the background, so remove it
        obj_ids = obj_ids[1:]

        # print("obj id's[]")
        # print(obj_ids)

        # split the color-encoded mask into a set
        # of binary masks
        masks = mask == obj_ids[:, None, None]
        
        
        # print(masks.shape)
        
        # get bounding box coordinates for each mask
        num_objs = len(obj_ids)
        boxes = []
        for i in range(num_objs):
            pos = np.where(masks[i])
            xmin = np.min(pos[1])
            xmax = np.max(pos[1])
            ymin = np.min(pos[0])
            ymax = np.max(pos[0])
            boxes.append([xmin, ymin, xmax, ymax])
            # if xmin - xmax < 1 :
            #     show(mask[i])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        # labels = torch.ones((num_objs,), dtype=torch.int64)

        labels = torch.as_tensor(obj_ids, dtype=torch.int64)

        # print("labels")
        # print(labels)
        # final_labels = []
        # for value in labels:
        #     # print(value.item())
        #     final_labels.append(value.item())
        # labels = torch.tensor(final_labels, dtype=torch.int64)


        masks = torch.as_tensor(masks, dtype=torch.uint8)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)

def get_model_instance_segmentation(num_classes):
    # load an instance segmentation model pre-trained pre-trained on COCO
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # now get the number of input features for the mask classifier
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    # and replace the mask predictor with a new one
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                       hidden_layer,
                                                       num_classes)

    return model


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)

# saves the model
def save_model(model):
    print('Saving Model...')
    torch.save(model, 'model.pt')
    print('Model Saved!')

def main():
    # train on the GPU or on the CPU, if a GPU is not available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    # our dataset has two(Changed to 3) classes only - background and person
    num_classes = 3
    # use our dataset and defined transformations
    dataset = ClawObjectDataset('Data', get_transform(train=True))
    dataset_test = ClawObjectDataset('Data', get_transform(train=False))

    # split the dataset in train and test set HERE
    indices = torch.randperm(len(dataset)).tolist()
    # print(indices)
    # print(indices[:-7])
    # print(indices[-7:])
    dataset = torch.utils.data.Subset(dataset, indices[-29:]) #changed from [:-50]
    dataset_test = torch.utils.data.Subset(dataset_test, indices[:-10]) #changed from [-50:]

    # define training and validation data loaders

    # print(dataset.__len__())

    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=1, shuffle=True, num_workers=2,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=2,
        collate_fn=utils.collate_fn)

    # get the model using our helper function
    model = get_model_instance_segmentation(num_classes)

    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005,
                                momentum=0.9, weight_decay=0.0005)
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1)

    # let's train it for 10 epochs
    num_epochs = 25

    for epoch in range(num_epochs):
        # train for one epoch, printing every 10 iterations
        train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=1)
        # update the learning rate
        lr_scheduler.step()
        # evaluate on the test dataset
        evaluate(model, data_loader_test, device=device)

    save_model(model)
    print("That's it!")
    
if __name__ == "__main__":
    main()