# Robot Arm Localization Usage

This is a description of how to install required packages and use the classes within this package

Python version: 3.8.11

## Installing Required Packages

1. Within this directory, run `pip3 install -r requirements.txt`

2. If this installation fails, try `pip3 install -r requirements_sample.txt`. This is a full output of the requirements from the conda environment but with the appropriate pip formatting.

3. (Note that there is an additional print out of entire conda environment if there are missing dependencies. in case of failure, create a new conda environment identical to the development environment use this command: `conda create --name robArmLocEnv --file full_requirements.txt`)

## Run the Demo

1. To run the demo, use the command `python3 run.py`

2. Note that included in this directory structure is a sample image as well as the model.

## Use inside of python interactive shell

1. To run inside of the python interactive shell, open the shell with `python3` and import the files as follows:

    - `from Vector import Vector`
    - `from DetectedObject import DetectedObject`
    - `from ObjectDetector import ObjectDetector`
    - `from Localizer import Localizer`
    - `import Utilities.utils as utils`

2. Load the image: `img = utils.load_image('frame_20.png')`

3. Load the depth values: `depth_arr = utils.load_depth_arr('frame_20_depth.npy')`

4. Send image to detector and run the model:
    -`detector = ObjectDetector(img)`
    -`detector.run()`

5. Create the localizer object:
    - `localizer = Localizer(detector, depth_arr)`

6. Investigate the detections and vectors:
    - `detector.claw`
    - `localizer.target_vector`

## Features

The demo illustrates the capabilities of the system thus far, including

- Runs model on submitted image and provides model outputs in the form of bounding boxes, Array masks, Labels, and scores

- Uses depth array from depth camera to calculate the average depth of the detections

- calculates position vectors for all detected objects in the image

- Calculates positions of target object relative to the robot arm base.

The demo also shows many visualization features of the system such as the depth array, the bounding boxes, the masks, the image, the centerpoints, and the masks overlayed over the image and depth data
