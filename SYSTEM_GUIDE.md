# Sign Language Recognition System - User Guide

## Overview
This is a real-time sign language recognition system using:
- **MediaPipe** for hand landmark detection
- **Dynamic Time Warping (DTW)** for gesture matching
- **OpenCV** for webcam input and display

## Features Implemented

### ✅ MODE 1: RECORD SIGN (Reference Data Creation)
Record custom sign gestures and save them as reference data for recognition.

**How to use:**
1. Run: `python main.py`
2. Choose mode: **1** (Record)
3. Enter sign name (e.g., "Hello", "Thanks", "Goodbye")
4. Press **'r'** to start recording
5. Perform the gesture for about 2 seconds (50 frames)
6. Press **'r'** again to finish and save
7. Saved to: `data/signs/<sign_name>/sequence_<timestamp>.npy`

**Recording Display:**
- "🎥 Recording Gesture... (X/50 frames)" - Status message

### ✅ MODE 2: RECOGNIZE SIGN (DTW Matching)
Recognize live gestures by comparing them against saved reference signs.

**How to use:**
1. Run: `python main.py`
2. Choose mode: **2** (Recognize) or press Enter (default)
3. Ensure reference signs are available (record some first if needed)
4. Press **'r'** to start recording a gesture
5. Perform the gesture for about 2 seconds (50 frames)
6. Press **'r'** again to finish
7. System compares against all saved signs using DTW
8. Best match is displayed on screen

**Recognition Display:**
- "🎥 Recording Gesture... (X/50 frames)" - Recording status
- "Recognized Sign: <label>" - Result displayed at bottom

### ✅ UI & Debug Features

**On-Screen Messages:**
- "Press 'r' to record/recognize | 'q' to quit" - Help text
- "🎥 Recording Gesture... (X/50 frames)" - Real-time recording progress
- "Recognized Sign: <label>" - Recognition result
- "No reference signs available" - Error message if no signs are saved

**Console Debug Output:**
- Number of loaded sign models on startup
- "Recording: X frames collected" - During recording
- "=== Processing sequence of X frames ===" - When DTW starts
- "DTW Distances: {...}" - Distance values for each sign
- "✓ Best match: 'sign_name' (distance: X.XXXX)" - Prediction result

**Keyboard Controls:**
- **'r'** - Start/stop recording
- **'q'** - Quit application

---

## System Architecture

### File Structure
```
data/
  signs/
    hello/
      sequence_20260121_010452.npy
      sequence_20260121_010459.npy
    thanks/
      sequence_20260121_011000.npy

models/
  hand_model.py       - Hand angle feature extraction
  pose_model.py       - Pose landmark handling
  sign_model.py       - Sign sequence model

utils/
  sign_storage.py     - Save/load reference sign sequences
  landmark_utils.py   - Extract hand landmarks from MediaPipe
  mediapipe_utils.py  - MediaPipe detection pipeline
  dtw.py              - Dynamic Time Warping distance computation
```

### Core Components

**1. SignRecorder (`sign_recorder.py`)**
- Manages both recording and recognition modes
- Saves gesture sequences to disk
- Loads reference signs from disk
- Computes DTW distances
- Implements voting mechanism for recognition

**2. WebcamManager (`webcam_manager.py`)**
- Displays webcam feed with hand landmarks
- Renders on-screen text using cv2.putText()
- Shows recording/recognition status
- Displays final predictions

**3. SignStorage (`utils/sign_storage.py`)**
- Saves landmark sequences as numpy arrays
- Loads saved signs with metadata
- Organizes signs by name in folders

---

## Technical Details

### Recording Process
1. **Frame Collection**: Collects 50 frames of MediaPipe hand landmarks
2. **Normalization**: Landmarks are normalized and stored as numpy arrays
3. **Persistence**: Sequences saved to `data/signs/<sign_name>/sequence_<timestamp>.npy`

### Recognition Process
1. **Baseline Recording**: Record 50 frames of live gesture
2. **Feature Extraction**: Extract hand angle features (HandModel)
3. **DTW Comparison**: Compute FastDTW distance vs. all reference signs
4. **Minimum Distance Selection**: Best match = sign with lowest DTW distance
5. **Voting**: Multiple reference sequences of same sign compared

### DTW Distance Metric
- Uses **FastDTW** algorithm for speed
- Compares hand angle feature vectors
- Handles variable-length sequences
- Distances computed separately for left and right hands

---

## Requirements
- Python 3.8+
- MediaPipe (v0.10.13)
- OpenCV
- NumPy
- FastDTW
- Pandas

**All dependencies**: Install with
```bash
pip install -r requirements_updated.txt
```

---

## Troubleshooting

**"No reference signs found"**
- Record some signs first in MODE 1

**Webcam not opening**
- Check if another application is using the webcam
- Try camera index 0 (default)

**Poor recognition accuracy**
- Record more reference examples for each sign
- Ensure consistent lighting and distance from camera
- Use clear, deliberate hand gestures

**Slow recognition**
- DTW computation is CPU-intensive
- Normal for first-time computation
- Caching can improve speed

---

## Future Enhancements
- Multi-hand gestures support
- Continuous recognition (without manual restart)
- Confidence threshold tuning
- Sign language dataset expansion
- GPU acceleration option

---

## Created: January 21, 2026
This system uses CPU-only processing and is compatible with standard laptops.
