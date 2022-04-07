# RobotArmLocalization
SE 490/491 Capstone Project. Robotic Arm and Object Localization.

## TrainingSrc/Utilities
Coco utilities for training, obtained from the following tutorial:
https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

## Istallation

This library requires at least Python Version 3, and is OS Independent.
    1. Begin by cloning this repository inside your workspace
    2. Download the model from https://drive.google.com/file/d/1LxqDJtm4NniyhlYb1Y9-I51jRiyY5A_o/view?usp=sharing
    3. place the model.pt file into src/arm-localizer/data/model/
    4. cd into the directory src/ directory with the setup.py file
    5. Within this directory, execute one of the following commands:
        a. Run pip3 install -r requirements.txt
        b. if this installations fails, try this:
            pip list --format=freeze requirements.txt
        c. To install in developer mode run: pip3 install -e . (developer mode sets a link to this directory, and allows for a live working copy to be used)
    6. Create a new conda environment identical to developement environment using this command: conda create --name robArmLocEnv --file full_requirements.txt
    
    ## Run Package
    

    ## usage
    1. To run inside of the python interactive shell, open shell with python3 and import files as follows:

            from arm-localizer import *
            
    2. Once your camera is setup, you will need to calibrate the arm-localizer. This is done by submitting image data, depth data, and the position(from the positioning system) of the claw, for two different claw positions

    3. You can get the images and depth value from the realsense camera
    4. Load the images: 
            img1 = Image.open('/path/to/img1/)
            img2 = Image.open('/path/to/img2/)

    5. Load the depth values:
            depth_arr1 = np.load(/path/to/deptharray1/)
            depth_arr2 = np.load(/path/to/deptharray2/) 

    6. Get the arm positions for each of the images(note that the arm must be in different positions) *The positioning system does not work. You will need to measure these values. The following code is how it is supposed to work but the solver does not work.
   
        ```from arm-controller import MechatronicsArm as MA
        arm = MA()
        pos1 = arm.get_pos()
        arm.move_to(new_position)
        pos2 = arm.get_pos()```

    7. Calibrate the system using arm-localizers calibrate function
        
        arm_localizer.calibrate(img1, depth_arr1, img2, depth_arr2, pos1, pos2)

    8. Now you can use the system to detect and transform the object in any image where the camera is in the same location. Just submit the depth and image you want to detect
        
        target = arm_localizer.get_object_position(img, depth)

    9.  You can also run the model independently using the ObjectDetector calss 
            - detector = ObjectDetector()  
            - detector.run(img)

    10. Get all the detections by from the detector
   
            - ds = detector.get_all_detections()

    11. Investigate the detections and vectors:

            - claw = detector.get_claw()
            - base = detector.get_base()
            - object = detector.get_object()

    12. Inspect the detections using visualizer methods
            - from arm_localizer import visualizer as viz
            - viz.show_mask(claw)
            - viz.show_boxes(ds)
            - viz.show_centerpoints(ds)
  
    13. Get the positions of the detections in millimeters

            - claw_pos = claw.rs_to_vector(depth).as_point()
            - base_pos = base.rs_to_vector(depth).as_point()


    ## Features

        1. Runs model on selected image and provides model outputs in form of bounding boxes, array masks, labels, and scores.

        2. Use depth array from depth camera to calculate average depth of the detections.

        3. Calculate position vectors for all detected Objects in image.

        4. Calculates positions of target Object relative to robot arm base.

        5. Calculates position of claw relative to robot arm base.

        6. Visualization features: depth array, bounding boxes, masks, images, centerpoints, masks overlayed over image, depth data.

        

            