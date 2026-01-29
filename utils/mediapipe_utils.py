import numpy as np

def mediapipe_detection(image, model):
    """
    Make holistic model prediction on image.

    :param image: Input image (numpy array)
    :param model: MediaPipe holistic model
    :return: Processed image and results
    """
    # Convert to RGB if needed (assuming input is BGR from PIL conversion)
    if image.shape[-1] == 3:
        image_rgb = image[:, :, ::-1]  # BGR to RGB
    else:
        image_rgb = image

    image_rgb.flags.writeable = False  # Image is no longer writeable
    results = model.process(image_rgb)  # Make prediction
    image_rgb.flags.writeable = True  # Image is now writeable

    # Return original image (BGR) and results
    return image, results
