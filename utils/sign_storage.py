"""
Module for saving and loading sign language reference sequences to/from disk.
Stores landmark sequences as numpy arrays with metadata.
"""

import os
import numpy as np
from datetime import datetime
import json


SIGNS_DIR = os.path.join("data", "signs")


def ensure_signs_directory():
    """Create the signs directory if it doesn't exist."""
    if not os.path.exists(SIGNS_DIR):
        os.makedirs(SIGNS_DIR, exist_ok=True)
    print(f"Signs directory: {SIGNS_DIR}")


def save_sign_sequence(sign_name, left_hand_list, right_hand_list):
    """
    Save a recorded gesture sequence to disk.
    
    :param sign_name: Name of the sign (e.g., "Hello")
    :param left_hand_list: List of left hand landmarks (sequence_length x 63)
    :param right_hand_list: List of right hand landmarks (sequence_length x 63)
    :return: Path to saved file
    """
    ensure_signs_directory()
    
    # Create sign-specific directory
    sign_dir = os.path.join(SIGNS_DIR, sign_name)
    if not os.path.exists(sign_dir):
        os.makedirs(sign_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sequence_{timestamp}.npy"
    filepath = os.path.join(sign_dir, filename)
    
    # Normalize and combine sequences
    data = {
        'sign_name': sign_name,
        'left_hand': np.array(left_hand_list, dtype=np.float32),
        'right_hand': np.array(right_hand_list, dtype=np.float32),
        'timestamp': timestamp,
        'sequence_length': len(left_hand_list)
    }
    
    # Save using numpy
    np.save(filepath, data, allow_pickle=True)
    
    print(f"✓ Saved sign '{sign_name}' ({len(left_hand_list)} frames) to {filepath}")
    return filepath


def load_all_sign_sequences():
    """
    Load all recorded sign sequences from disk.
    
    :return: Dictionary mapping sign_name -> list of (left_hand, right_hand) tuples
    """
    ensure_signs_directory()
    
    sign_sequences = {}
    
    if not os.path.exists(SIGNS_DIR):
        print(f"No signs directory found at {SIGNS_DIR}")
        return sign_sequences
    
    # Iterate through each sign folder
    for sign_name in os.listdir(SIGNS_DIR):
        sign_path = os.path.join(SIGNS_DIR, sign_name)
        if not os.path.isdir(sign_path):
            continue
        
        sign_sequences[sign_name] = []
        
        # Load all .npy files in this sign's folder
        for filename in os.listdir(sign_path):
            if filename.endswith('.npy'):
                filepath = os.path.join(sign_path, filename)
                try:
                    data = np.load(filepath, allow_pickle=True).item()
                    left_hand = data['left_hand']
                    right_hand = data['right_hand']
                    sign_sequences[sign_name].append((left_hand, right_hand))
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    
    total_sequences = sum(len(sequences) for sequences in sign_sequences.values())
    print(f"✓ Loaded {total_sequences} sign sequences from {len(sign_sequences)} signs")
    
    return sign_sequences


def get_available_signs():
    """
    Get list of available sign names.
    
    :return: List of sign names
    """
    ensure_signs_directory()
    
    if not os.path.exists(SIGNS_DIR):
        return []
    
    signs = [d for d in os.listdir(SIGNS_DIR) if os.path.isdir(os.path.join(SIGNS_DIR, d))]
    return sorted(signs)
