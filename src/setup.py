# This file is the build script for setuptools. Gives information about package,
# tells which code files to include. 

import setuptools

with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()

setuptools.setup(
    name = "arm_localizer",
    version="0.0.4",
    author="SE490 Fall, SE491 Spring 2021-22 SCSU Capstone John Deere Team",
    description="Robot Arm and Object Localization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KrickLogan/RobotArmLocalization",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"

    ],

    # package_dir={'': 'arm_localizer'},
    
    packages = [
        "arm_localizer",
        "arm_localizer.data",
        "arm_localizer.utilities",
        "arm_localizer.data.model"
    ],

    package_data = {
        'arm_localizer.data.model': [ 'model.pt' ],                 
    }

)