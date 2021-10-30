# How to Train the Model

## 1. Directories

---

### 1.1 The Project Directory
The Project Directory is the root directory of the project:
* `RobotArmLocalization\`

---

### 1.2 The Training Directory
Everything for training the model is located in the following directory:
* `RobotArmLocalization\src\TrainingSrc\`

---

### 1.3 The Utilities Directory
Our training script depends on files from the Utilities Directory, which is located at the following path:
* `RobotArmLocalization\src\TrainingSrc\Utilities`

The files located in the Utilities directory are required for running the training script, but do not require any modification.

---

### 1.4 Data Directory
Inside the the Data directory `RobotArmLocalization\src\TrainingSrc\Data` we have the following directories:
* `RobotArmLocalization\src\TrainingSrc\Data\PNGMasks`
* `RobotArmLocalization\src\TrainingSrc\Data\PNGImages`

Place all created Masks inside the `\PNGMasks` directory and all images corresponding to the created masks inside the `\PNGImages` directory. The images and masks in these directories will be used for training the model.

---

## 2. Training the Model

---

### 2.1 Input Data
Place all created masks and their corresponding image files in the `Data` directory as specified in `Section 1.4`.

---

### 2.2 Modifying the Training Script
The training script is located in the `Training Directory` as specified in `Section 1.2`. The script for training the model is `model-training-code.py`. There are plenty of comments in this script that give more information about what each part of the training script does, please check them out for a more detailed overview of the training script.

**Important parts of the training script:**

#### `Lines 55-57:`
```
# convert grayscale values of masks to contiguous integer values from 0 to number of classes

for i in range(len(obj_ids)):
    mask = np.where(mask == obj_ids[i], i, mask)
```
This model uses unique values inside of the mask array to know which mask “contains” which object. The grayscale values of the masks coming from gimp are between `0` and `255`, these lines convert them to be integers in the range of the number of classes *(see line 144)*. The unique values in these masks, if the masking procedure is followed, change from `[0, 64, 127, 255]` to `[0, 1, 2, 3]`. This is what the model expects for classifications. The array which contains the object ids is also changed in this manner.

#### `Line 107:`
```
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
```
The `model` we will be starting with is a pre-trained maskrcnn_resnet50_fpn. We will train our own model on top of this pre-trained model.

#### `Line 144:`
```
num_classes = 4
```
The `num_classes` variable is the number of classifications in the model. We currently have four classes:
1. Background
2. Base
3. Claw
4. Cotton

#### `Line 150:`
```
test_split = 0.2
```
The `test_split` variable defines what percentage of the dataset should be allocated to the testing dataset. The remaining percentage of the dataset will be used for the training dataset.'

#### `Line 182:`
```
num_epochs = 15
```
The `num_epochs` variable specifies how many epochs to train the model for. The number of epochs indicates the number of passes of the entire training dataset the machine learning algorithm is to complete. Currently it is set to complete 15 epochs, but may be changed to however many epochs you would like to train for.

#### `Line 186:`
```
train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)
```
Depending on your dataset size, you may want to change the `print_freq` parameter to limit the amount of prints inside each epoch. With a `print_freq` value equal to 10 the model will print information about every 10th image in each epoch.

### 2.3 Running the Training Script
Once your masks and image files are in their appropriate directories (covered in `Section 2.1`) and you have finished modifying the training script to your needs (covered in `Section 2.2`) you are ready to train the model. Simply run the training script, `model-training-code.py`.

Navigate to the Project Directory (`Section 1.1`) and run the following command from a command prompt or terminal:
```
python3 src\TrainingSrc\model-training-code.py
```
Once the training script is finished training, the model will be saved in the Project Directory (`Section 1.1`) as the following file:
* `model.pt`
