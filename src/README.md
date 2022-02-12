# RobotArmLocalization
SE 490/491 Capstone Project. Robotic Arm and Object Localization.

## TrainingSrc/Utilities
Coco utilities for training, obtained from the following tutorial:
https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

## Istallation

This library requires at least Python Version 3, and is OS Independent.
    1. Begin by cloning this repository inside your workspace
    2. cd into the directory
    3. Within this directory, execute one of the following commands:
        a. Run pip3 install -r requirements.txt
        b. if this installations fails, try this:
            pip list --format=freeze requirements.txt
        c. To install in developer mode run: pip3 install -e . (developer mode sets a link to this directory, and allows for a live working copy to be used)
    4. Create a new conda environment identical to developement environment using this command: conda create --name robArmLocEnv --file full_requirements.txt
    
    ## Run Package
    1. Use command: python3 run.py

    2. Note that included in this directory structure is a sample image as well as the model.

    ## usage
    1. To run inside of the python interactive shell, open shell with python3 and import files as follows:

            from Vector import Vector

            from DetectedObject import DetectedObject

            from ObjectDetector import ObjectDetector

            from Localizer import Localizer

            import Utilities.utils as utils

            
    2. Load the image: 
            img = utils.load_image('frame_20.png')

    3. Load the depth values:
            depth_arr = utils.load_depth_arr('frame_20_depth.npy')

    4. Send image to detector and run the model: 
            - detector = ObjectDetector(img) - detector.run()

    5. Create the localizer Object:
            localizer = Localizer(detector, depth_arr)

    6. Investigate the detections and vectors:

            detector.claw

            localizer.target_vector


    ## Features

        1. Runs model on selected image and provides model outputs in form of bounding boxes, array masks, labels, and scores.

        2. Use depth array from depth camera to calculate average depth of the detections.

        3. Calculate position vectors for all detected Objects in image.

        4. Calculates positions of target Object relative to robot arm base.

        5. Calculates position of claw relative to robot arm base.

        6. Visualization features: depth array, bounding boxes, masks, images, centerpoints, masks overlayed over image, depth data.

        

            