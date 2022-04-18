# RobotArmLocalization

Robotic Arm and Object Localization, an SE 490/491 Capstone Project.

## TrainingSrc/Utilities

Coco utilities for training were obtained from the following tutorial:
https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

## Requirements

- torch==1.9.0
- torchvision==0.10.0
- matplotlib>=3.4.3
- numpy>=1.21.2
- pillow>=8.3.2
- scipy>=1.7.3
- pyrealsense2>=2.50.0.3812

## Windows Installation

This library requires at least Python Version 3.8.11.
1. Begin by cloning this repository inside your workspace
2. Download the model from https://drive.google.com/file/d/1LxqDJtm4NniyhlYb1Y9-I51jRiyY5A_o/view?usp=sharing
3. Place the model.pt file into src/arm-localizer/data/model/
4. `cd` into the `RobotArmLocalization/src/` directory where the setup.py file is located
5. Within this directory, execute one of the following commands:
   1. Run `pip3 install .`
   2. To install in developer mode run: `pip3 install -e .`  
        *(Developer mode sets a link to this directory, and allows for a live working copy to be used)*
6. *Optionally*, create a new conda environment identical to developement environment using this command: `conda create --name robArmLocEnv --file full_requirements.txt`

## Raspberry Pi Installation

This library requires at least Python Version 3.8.11.
1. Begin by cloning this repository inside your workspace
2. Download the model from https://drive.google.com/file/d/1LxqDJtm4NniyhlYb1Y9-I51jRiyY5A_o/view?usp=sharing
3. Place the model.pt file into src/arm-localizer/data/model/
4. `cd` into the `RobotArmLocalization/src/` directory where the setup.py file is located
5. Within this directory, execute one of the following commands:
   1. Run `pip3 install .`
   2. To install in developer mode run: `pip3 install -e .`  
        *(Developer mode sets a link to this directory, and allows for a live working copy to be used)*
6. *Optionally*, create a new conda environment identical to developement environment using this command: `conda create --name robArmLocEnv --file full_requirements.txt`

## Running the Package

### Features

1. Runs the model on a selected image and provides model outputs in form of bounding boxes, array masks, labels, and scores.

2. Use the depth array from a depth camera to calculate average depth of the detections.

3. Calculates the position vectors for all detected Objects in image.

4. Calculates the position of the target Object relative to robot arm base and in alignment with the `arm_controller` package's coordinate system.

5. Calculates the position of the Robot Arm Claw relative to Robot Arm Base.

6. Visualization Features: depth array, bounding boxes, masks, images, centerpoints, masks overlayed over image, depth data analysis.

### Usage

1. To run inside of the python interactive shell, open shell with `python3` and import files as follows:

        from arm_localizer import *
            
2. Once your camera is setup, you will need to calibrate the `arm_localizer`. This is done by submitting image data, depth data, and the position of the claw (from the positioning system), for two different claw positions

3. You can get the images and depth values from the realsense camera

4. Load the images:

        img1 = Image.open('/path/to/img1/)
        img2 = Image.open('/path/to/img2/)

5. Load the depth values:

        depth_arr1 = np.load(/path/to/deptharray1/)
        depth_arr2 = np.load(/path/to/deptharray2/) 

6. Get the arm positions for each of the images (note that the arm must be in different positions). **The positioning system used by the `arm_controller` package may be inconsistent.** You may need to measure these values yourself. The following code is how `arm_controller` is supposed to work, but the solver does not work consistently.
   
        from arm_controller import MechatronicsArm as MA
        arm = MA()
        pos1 = arm.get_pos()
        arm.move_to(new_position)
        pos2 = arm.get_pos()

7. Calibrate the system using `arm_localizer`'s `rs_calibrate()` function:
        
        arm_localizer.rs_calibrate(img1, depth_arr1, img2, depth_arr2, pos1, pos2)

8. You have now successfully calibrated the `arm_localizer`. **Please Note, if the camera is moved you must recalibrate `arm_localizer` by performing step 7 again.** You can now use the system to detect and transform the object in any image. Just submit the image and depth you want to detect:
        
        object_position = arm_localizer.get_object_position(img, depth)

9.  You may also run the model independently using the `ObjectDetector` class 

        detector = ObjectDetector()  
        detector.run(img)

- *Optionally*, you may set the threshold values used for each type of `DetectedObject` when declaring a new `ObjectDetector`

  - Threshold values must be between 0 and 1.
  - Default threshold value is 0.5.

        detector = ObjectDetector(threshold_claw = 0.5, threshold_base = 0.5, threshold_object = 0.5)

10. Get all of the detections from the detector:
   
        all_detections = detector.get_all_detections()

11. Investigate the detections and vectors:

        claw = detector.get_claw()
        base = detector.get_base()
        obj = detector.get_object()

12. Inspect the detections using visualizer methods:

        from arm_localizer import visualizer as viz
        ...
        viz.show_all_masks(all_detections)
        viz.show_all_boxes(all_detections)
        viz.show_all_centerpoints(all_detections)
  
13. Get the positions of the detections in millimeters

        claw_pos = claw.rs_to_vector(depth).as_point()
        base_pos = base.rs_to_vector(depth).as_point()
