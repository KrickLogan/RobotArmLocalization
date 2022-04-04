from arm_localizer import ObjectDetector
import arm_localizer.utilities.utils as utils
import arm_localizer.utilities.visualizer as viz
import matplotlib.pyplot as plt

def main():
    frame_prefix = "frame_20"   
    img = utils.load_image(frame_prefix + ".png")   #open and load image as img
    plt.imshow(img)
    plt.show()

    detector = ObjectDetector() # provide image to model
    
    detector.run(img) # run model on provided image

    # Get output for each of the detections

    detections = detector.get_all_detections() #get all the detections from model as detections
    obj = detector.get_object()  #get detection for object
    claw = detector.get_claw()     #get detection for claw
    base = detector.get_base()   #get detection for base

    # Visualize detections

    viz.show_img_boxes(img, detections) #Show all the detection in a frame
    viz.show_img_box(img, obj)    #show object detection in a frame
    viz.show_img_box(img, claw)    #show claw detection in a frame
    viz.show_img_box(img, base)    #show base detection in a frame

if __name__ == "__main__":
    main()
