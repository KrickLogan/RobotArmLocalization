from arm_localizer import ObjectDetector
import arm_localizer.utilities.utils as utils
import matplotlib.pyplot as plt

def main():
    frame_prefix = "frame_20"   
    img = utils.load_image(frame_prefix + ".png")
    plt.imshow(img)
    plt.show()

    # provide image to model
    detector = ObjectDetector()
    
    # run model on provided image
    detector.run(img) 

    # The following get the output of all detections
    detections = detector.get_all_detections()
    for det in detections:
        print(f"{det.label} Score: {det.score} Box: {det.box} Mask: {det.mask}" )

    # The following prints all model outputs
    output = detector.get_model_outputs()
    print (output)
    

if __name__ == "__main__":
    main()
