# *Masking Procedure Using GIMP*

## This document was developed by SCSU SE490 students in the capstone project in the fall 2021 semester for John Deere Electronics Solutions.

---
###  Gimp Tools and their settings:

- Select (Rectangle, scissors, magic wand, etc.)
- Antialiasing: OFF

- Magic Wand color selector
- Threshold: Higher means more general Selection of like colors, Lower- more specific ( set around 88 - 108)
- Modes: Can be Union, Intersect, 

- TIPS:  To switch between tools, (Fuzzy Select, COlor select for example) Right click or ctrl click on the button and the other options will drop down.
- Bucket fill: Set to Fill Whole Selection
- Antialiasing: OFF

- Color Pallet:Click on one of the colored squares to select a different color. Can right click left click for fg/bg color
---
#### General Settings(Might be best practice to make these changes after editing the mask)

- (From Toolbar) Image > Mode > Grayscale
- (From Toolbar) Layer > Transparency > Remove Alpha Channel

---



##### Detailed instructions:
1. Open image.

2. Toolbar: File > Save As > “frame_###_mask.xcf” (add “_mask” to the filename)

3. Using Free Select Tool (Mode: Replace), trace outline around robot claw

4. Using Fuzzy Select Tool (Mode: Intersect), click inside the outline

5. Using Bucket Fill Tool (Color: Gray), click inside the outline 

6. Using Free Select Tool (Mode: Replace), trace outline around cotton

7. Repeat Step 4

8. Repeat Step 5 (Color: White)

9. Using Free Select Tool (Mode: Replace), trace outline around robot base

10. Repeat Step 4

11. Repeat Step 5 (Color: Dark)

12. Using Fuzzy Select Tool (Mode: Add) (Threshold: 0), click 
13. on robot claw, click on cotton

14. Right click on the image, Select > Invert

15. Using Bucket Fill Tool (Color: Black), click on the image, not on the two colored objects

16. Toolbar: Image > Mode > Grayscale

17. Toolbar: Layer > Transparency > Remove Alpha Channel

18. Toolbar: File > Save/Save As

19. Toolbar: File > Export As

------
###### Alternatives

1. Open the image you wish to mask

2. Save the image, adding _mask to the filename. This is so that our program can identify this image as being a mask.
3. With the Free Select Tool, trace an outline around the object. This example will use the robot claw, but steps 3-5 must be repeated for each object you wish to mask. 

4. After an outline has been traced around the object, you can utilize the Fuzzy Select or Free Select Tools (in various modes), to try and clean up the outline, making it match the object more accurately. 

5. Once the outline has been cleaned up, use the Bucket Fill Tool to fill the outline with a solid color. For the robot claw, this is Gray, denoted by a K value of 50. 

6. Once all objects have been masked with steps 3-5, use the Fuzzy Select Tool (Mode:Add) (Threshold:0) to select all the objects at once. 

7. Invert the objects you have selected. This can be done with the toolbar or by right clicking on the image.  

8. Alternatively, you can use Ctrl + I

9. Use the Bucket Fill Tool to fill the background with black.

10. Using the top toolbar, select the following options. These are necessary steps so that our program can retrieve all the correct data from your masks.

    - Image > Mode > Grayscale
    - Layer > Transparency > Remove Alpha Channel

11. Save and export the mask using the File toolbar. No options need to be modified from Gimp’s defaults when exporting the mask. 

---





###### Colors

- Mask the “cotton object” with WHITE, K=0
- Mask the “robot claw” with Light Gray, K=50
- Mask the Base (Cylinder) of the Arm with Dark Gray, K=75
- Fill the background with Black, K=100
- To set color, Open Color pallet, CMYK tab, White: K = 0, Light Gray: - K=50, Dark Gray: K=75, Black: K = 100

![image](https://www.linkpicture.com/q/cmyk.jpg)
- Remove Alpha Channel
- Change to Gray Scale
- Make sure Antialiasing is Always OFF




---

####### Example

- Background not filled in to give a better idea
![image](https://www.linkpicture.com/q/mask.png)

- final mask:
![image](https://www.linkpicture.com/q/frame_57_mask.png)



