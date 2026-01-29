import cv2
import mediapipe as mp

def mediapipe_detection(image, model):
    """
    Make holistic model prediction on image.
    
    :param image: Input image (numpy array)
    :param model: MediaPipe holistic model
    :return: Processed image and results
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
    return image, results
