# This file is the build script for setuptools. Gives information about package,
# tells which code files to include. 

import setuptools

with open("../README.md", "r", encoding="utf-8") as fh: long_description = fh.read()

setuptools.setup(
    name = "arm_localizer",
    version="0.1.0",
    author="SE490 Fall, SE491 Spring 2021-22 SCSU Capstone John Deere Team",
    description="Robot Arm and Object Localization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KrickLogan/RobotArmLocalization",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    
    packages = [
        "arm_localizer",
        "arm_localizer.data.model",
        "arm_localizer.utilities"
    ],

    package_data = {
        'arm_localizer.data.model': [ 'model.pt' ],                 
    },

    install_requires=[
        "torch==1.9.0",
        "torchvision==0.10.0",
        "matplotlib>=3.4.3",
        "numpy>=1.21.2",
        "pillow>=8.3.2",
        "scipy>=1.7.3",
        # For Mac, there is no pip package for pyrealsense2 you have to build from source. 
        #   Comment out the following line, build from source, then symlink into the conda environment
        #   if you are using a conda environment
        "pyrealsense2>=2.50.0.3812"
    ],

    python_requires=">=3.7"

)