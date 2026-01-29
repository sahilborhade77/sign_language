import numpy as np
from fastdtw import fastdtw

def dtw_distances(recorded_seq, reference_seqs):
    """
    Compute DTW distances between recorded sequence and reference sequences.
    
    :param recorded_seq: Recorded sequence
    :param reference_seqs: List of reference sequences
    :return: List of distances
    """
    distances = []
    for ref_seq in reference_seqs:
        distance, _ = fastdtw(recorded_seq, ref_seq)
        distances.append(distance)
    return distances
