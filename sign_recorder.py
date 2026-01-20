import pandas as pd
import numpy as np
from collections import Counter

from utils.dtw import dtw_distances
from models.sign_model import SignModel
from utils.landmark_utils import extract_landmarks
from utils.sign_storage import save_sign_sequence, load_all_sign_sequences


class SignRecorder(object):
    def __init__(self, reference_signs: pd.DataFrame = None, seq_len=50, mode="recognize", dtw_threshold=2000):
        """
        Initialize SignRecorder.
        
        :param reference_signs: DataFrame with reference signs (for recognize mode)
        :param seq_len: Number of frames to record per gesture
        :param mode: "record" to create reference signs, "recognize" to match against saved signs
        :param dtw_threshold: Maximum DTW distance to consider a valid match (default 2000)
        """
        # Variables for recording
        self.is_recording = False
        self.is_saving = False
        self.seq_len = seq_len
        self.mode = mode
        self.dtw_threshold = dtw_threshold

        # List of results stored each frame
        self.recorded_results = []
        
        # For saving: store the sign name during recording
        self.current_sign_name = None
        
        # Store last DTW distance for display
        self.last_dtw_distance = None

        # DataFrame storing the distances between the recorded sign & all the reference signs from the dataset
        self.reference_signs = reference_signs if reference_signs is not None else pd.DataFrame()
        
        # Load reference sign sequences from disk
        self.sign_sequences = load_all_sign_sequences()
        self.num_loaded_signs = len(self.sign_sequences)
        
        print(f"✓ SignRecorder initialized in '{mode}' mode")
        print(f"✓ DTW threshold set to {dtw_threshold}")
        print(f"✓ Loaded {self.num_loaded_signs} reference signs")

    def record(self, sign_name=None):
        """
        Start recording a new gesture sequence.
        
        :param sign_name: Name of the sign to record (required for recording mode)
        """
        if self.mode == "record":
            if sign_name is None:
                raise ValueError("sign_name is required in record mode")
            self.current_sign_name = sign_name
            self.is_saving = True
            print(f"\n📹 Recording '{sign_name}'... Press 'r' again to finish")
        else:
            # In recognize mode, start recording for recognition
            self.is_recording = True
            print(f"\n📹 Recording gesture for recognition... ({0}/{self.seq_len} frames)")

    def process_results(self, results) -> (str, bool):
        """
        Process mediapipe results and manage recording/recognition.
        
        :param results: mediapipe output
        :return: Tuple of (predicted_text, is_recording, recording_mode)
        """
        # Handle recording mode (saving reference signs)
        if self.is_saving:
            if len(self.recorded_results) < self.seq_len:
                self.recorded_results.append(results)
            else:
                self._save_sign()
                return f"Saved: {self.current_sign_name}", self.is_saving

        # Handle recognize mode (matching against reference signs)
        if self.is_recording:
            if len(self.recorded_results) < self.seq_len:
                self.recorded_results.append(results)
            else:
                predicted_text = self._compute_distances_and_predict()
                return predicted_text, self.is_recording

        return "", self.is_recording

    def _save_sign(self):
        """Save the recorded gesture sequence to disk."""
        if self.current_sign_name is None:
            print("Error: No sign name set")
            return

        left_hand_list, right_hand_list = [], []
        for results in self.recorded_results:
            _, left_hand, right_hand = extract_landmarks(results)
            left_hand_list.append(left_hand)
            right_hand_list.append(right_hand)

        # Save to disk
        save_sign_sequence(self.current_sign_name, left_hand_list, right_hand_list)

        # Reset recording state
        self.recorded_results = []
        self.is_saving = False
        self.current_sign_name = None

    def _compute_distances_and_predict(self) -> str:
        """
        Compute DTW distances and predict the sign.
        Apply DTW threshold to filter out poor matches.
        
        :return: Predicted sign name or "Unknown Sign"
        """
        # Check if we have reference signs
        if self.num_loaded_signs == 0:
            print("⚠ No reference signs found. Record some signs first using 'record' mode.")
            self.recorded_results = []
            self.is_recording = False
            self.last_dtw_distance = None
            return "No reference signs"

        print(f"\n=== Processing sequence of {len(self.recorded_results)} frames ===")

        left_hand_list, right_hand_list = [], []
        for results in self.recorded_results:
            _, left_hand, right_hand = extract_landmarks(results)
            left_hand_list.append(left_hand)
            right_hand_list.append(right_hand)

        # Create a SignModel object with the landmarks gathered during recording
        recorded_sign = SignModel(left_hand_list, right_hand_list)

        # Compute DTW distances against all reference signs
        distances = {}
        for sign_name, sequences in self.sign_sequences.items():
            min_distance = float('inf')
            for ref_left, ref_right in sequences:
                # ref_left and ref_right are full sequences (arrays of shape (seq_len, 63))
                # Convert them to list format for SignModel
                ref_sign = SignModel(ref_left.tolist(), ref_right.tolist())
                # Compute DTW distance
                dist = self._compute_dtw_distance(recorded_sign, ref_sign)
                min_distance = min(min_distance, dist)
            distances[sign_name] = min_distance

        # Find the best match
        if distances:
            best_sign = min(distances, key=distances.get)
            best_distance = distances[best_sign]
            
            print(f"DTW Distances: {distances}")
            print(f"Best match: '{best_sign}' (distance: {best_distance:.2f})")
            
            # Store distance for display
            self.last_dtw_distance = best_distance
            
            # Check if distance is below threshold
            if best_distance > self.dtw_threshold:
                print(f"⚠ Distance {best_distance:.2f} exceeds threshold {self.dtw_threshold}")
                print("→ Classified as 'Unknown Sign'")
                best_sign = "Unknown Sign"
        else:
            best_sign = "Unknown Sign"
            self.last_dtw_distance = None

        # Reset recording state
        self.recorded_results = []
        self.is_recording = False

        return best_sign

    def _compute_dtw_distance(self, sign1: SignModel, sign2: SignModel) -> float:
        """
        Compute DTW distance between two sign models using FastDTW.
        """
        from fastdtw import fastdtw
        
        # Get embeddings
        emb1_left = sign1.lh_embedding if sign1.has_left_hand else []
        emb1_right = sign1.rh_embedding if sign1.has_right_hand else []
        emb2_left = sign2.lh_embedding if sign2.has_left_hand else []
        emb2_right = sign2.rh_embedding if sign2.has_right_hand else []
        
        total_distance = 0
        
        # Compute DTW for left hand if both have it
        if sign1.has_left_hand and sign2.has_left_hand and len(emb1_left) > 0 and len(emb2_left) > 0:
            dist, _ = fastdtw(emb1_left, emb2_left)
            total_distance += dist
        
        # Compute DTW for right hand if both have it
        if sign1.has_right_hand and sign2.has_right_hand and len(emb1_right) > 0 and len(emb2_right) > 0:
            dist, _ = fastdtw(emb1_right, emb2_right)
            total_distance += dist
        
        return total_distance if total_distance > 0 else float('inf')

    def stop_recording(self):
        """Stop recording without saving."""
        self.is_recording = False
        self.is_saving = False
        self.recorded_results = []
        print("Stopped recording")
