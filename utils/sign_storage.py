import os
import pickle
import numpy as np

SIGNS_DIR = "data/signs"

def save_sign_sequence(sign_name, left_hand_list, right_hand_list):
    """
    Save a sign sequence to disk.
    
    :param sign_name: Name of the sign
    :param left_hand_list: List of left hand landmarks
    :param right_hand_list: List of right hand landmarks
    """
    if not os.path.exists(SIGNS_DIR):
        os.makedirs(SIGNS_DIR)
    
    filename = f"{SIGNS_DIR}/{sign_name}.pkl"
    data = {
        'left_hand': left_hand_list,
        'right_hand': right_hand_list
    }
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print(f"Saved sign '{sign_name}' to {filename}")

def load_all_sign_sequences():
    """
    Load all saved sign sequences from disk.
    
    :return: Dictionary of sign_name -> list of (left_hand, right_hand) sequences
    """
    sequences = {}
    if not os.path.exists(SIGNS_DIR):
        return sequences
    
    for filename in os.listdir(SIGNS_DIR):
        if filename.endswith('.pkl'):
            sign_name = filename[:-4]
            filepath = os.path.join(SIGNS_DIR, filename)
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            sequences[sign_name] = [(np.array(data['left_hand']), np.array(data['right_hand']))]
    return sequences

def get_available_signs():
    """
    Get list of available sign names.
    
    :return: List of sign names
    """
    if not os.path.exists(SIGNS_DIR):
        return []
    return [f[:-4] for f in os.listdir(SIGNS_DIR) if f.endswith('.pkl')]
