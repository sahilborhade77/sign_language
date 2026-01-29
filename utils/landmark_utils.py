import numpy as np

def extract_landmarks(results):
    """
    Extract hand landmarks from MediaPipe results.
    
    :param results: MediaPipe holistic results
    :return: Tuple of (pose, left_hand, right_hand) landmarks
    """
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(132)
    
    left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(63)
    
    right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(63)
    
    return pose, left_hand, right_hand
