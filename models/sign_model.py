import numpy as np

class SignModel:
    def __init__(self, left_hand_list, right_hand_list):
        """
        Initialize SignModel with hand landmark sequences.
        
        :param left_hand_list: List of left hand landmarks (list of 63-element arrays)
        :param right_hand_list: List of right hand landmarks (list of 63-element arrays)
        """
        self.left_hand_list = np.array(left_hand_list) if left_hand_list else np.array([])
        self.right_hand_list = np.array(right_hand_list) if right_hand_list else np.array([])
        
        # Check if hands are present
        self.has_left_hand = len(self.left_hand_list) > 0 and np.any(self.left_hand_list != 0)
        self.has_right_hand = len(self.right_hand_list) > 0 and np.any(self.right_hand_list != 0)
        
        # Create embeddings (simplified - just flatten the sequences)
        self.lh_embedding = self.left_hand_list.flatten() if self.has_left_hand else []
        self.rh_embedding = self.right_hand_list.flatten() if self.has_right_hand else []
