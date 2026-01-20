# Sign Language Recognition System

A real-time sign language recognition system built with Python, MediaPipe, and Dynamic Time Warping (DTW). Record custom sign gestures and recognize them in real-time with voice feedback.

## Features

✨ **Real-Time Recognition** - Instantly recognize recorded signs from webcam input  
🎙️ **Voice Output** - Offline text-to-speech feedback for recognized signs  
🎬 **Custom Sign Recording** - Record and save your own sign gestures  
🔄 **Mode Switching** - Seamlessly toggle between recording and recognition modes  
⚙️ **Quality Control** - DTW threshold filtering for accurate recognition  
🎯 **Professional UI** - Clear status display and intuitive keyboard controls  
💻 **CPU-Based** - Runs efficiently on standard laptops without GPU  

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd sign_language

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements_updated.txt
```

### Run the Application

```bash
python main.py
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `r` | Record/Stop gesture |
| `m` | Toggle RECORD/RECOGNIZE mode |
| `n` | Record new sign (name input) |
| `q` | Quit application |

## How It Works

### Recording Mode
1. Press `m` to enter RECORD mode
2. Press `n` to start recording a new sign
3. Enter the sign name when prompted
4. Press `r` to begin capturing
5. Perform the gesture (aim for ~2 seconds)
6. Press `r` again to save

### Recognition Mode
1. Make sure you're in RECOGNIZE mode (press `m` if needed)
2. Press `r` to start recognition
3. Perform a recorded gesture
4. Press `r` to stop
5. The system will display the recognized sign and speak it aloud

## Technologies Used

- **OpenCV** - Real-time video capture and display
- **MediaPipe** - Hand and pose landmark detection
- **Dynamic Time Warping (DTW)** - Gesture sequence matching and similarity computation
- **NumPy** - Numerical operations and array manipulation
- **pyttsx3** - Offline text-to-speech synthesis

## Project Structure

```
sign_language/
├── main.py                    # Application entry point
├── sign_recorder.py           # Core recognition and recording logic
├── webcam_manager.py          # Video display and UI rendering
│
├── utils/
│   ├── voice_output.py        # Text-to-speech interface
│   ├── sign_storage.py        # Save/load sign data
│   ├── landmark_utils.py      # Hand landmark extraction
│   ├── mediapipe_utils.py     # MediaPipe pipeline
│   └── dtw.py                 # DTW distance computation
│
├── models/
│   ├── hand_model.py          # Hand angle feature extraction
│   ├── pose_model.py          # Pose landmark handling
│   └── sign_model.py          # Sign sequence processing
│
└── data/
    └── signs/                 # Saved custom sign data
```

## System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Camera:** Standard webcam
- **RAM:** Minimum 4GB (8GB recommended)
- **CPU:** Standard dual-core processor or better
- **GPU:** Not required (CPU-based)

## Performance

- **Recording:** Captures 50 frames (~2 seconds)
- **Recognition:** 0.5-2 seconds per gesture
- **Voice Output:** Instant (background thread)
- **Frame Rate:** ~25 FPS on standard CPU
- **Memory Usage:** ~50MB for loaded signs

## Configuration

### Adjusting DTW Threshold

The DTW threshold controls recognition sensitivity. Edit in `sign_recorder.py`:

```python
self.dtw_threshold = 2000  # Lower = stricter, Higher = lenient
```

### Voice Output Settings

Customize voice in `utils/voice_output.py`:

```python
self.engine.setProperty('rate', 150)      # Speed in WPM
self.engine.setProperty('volume', 0.9)    # Volume 0-1
```

## Documentation

- **[QUICKREF_V2.md](QUICKREF_V2.md)** - Quick reference card with all controls
- **[UPGRADE_GUIDE_V2.md](UPGRADE_GUIDE_V2.md)** - Detailed feature documentation
- **[MASTER_SUMMARY_V2.md](MASTER_SUMMARY_V2.md)** - Complete project overview

## Future Enhancements

Planned features marked in code (see TODO comments):

- **Static Alphabet Recognition** - A-Z sign recognition
- **Speech-to-Sign Translation** - Convert spoken words to signs
- **Advanced ML Classifier** - Improved gesture classification
- **Sign Language Database** - Pre-built gesture library

## Troubleshooting

### Webcam Not Opening
- Ensure no other application is using the camera
- Check camera permissions in system settings
- Try restarting the application

### Voice Not Working
- Verify pyttsx3 is installed: `pip install pyttsx3`
- Check system volume is not muted
- On Windows, ensure text-to-speech engine is installed

### Poor Recognition
- Ensure adequate lighting
- Perform gestures clearly and consistently
- Consider lowering the DTW threshold for stricter matching
- Record multiple examples of each sign

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

---

# Acknowledgements

This project was developed with the assistance of **GitHub Copilot**, which served as a coding assistant throughout the development process. Copilot was utilized for:
- Debugging and troubleshooting implementation issues
- Code refactoring and structural improvements
- Feature development and extension
- Code documentation and best practices

## Project Inspiration

The initial concept and technical foundation for real-time gesture recognition were inspired by the open-source repository **[Sign-Language-Recognition--MediaPipe-DTW](https://github.com/gabguerin/Sign-Language-Recognition--MediaPipe-DTW)** by [gabguerin](https://github.com/gabguerin). That repository was invaluable for understanding:
- MediaPipe-based hand landmark detection and extraction
- Dynamic Time Warping (DTW) for sequence-based gesture matching
- End-to-end pipeline architecture for sign recognition

## Original Implementation

While conceptually inspired by the above work, this repository contains **significant original modifications and features**, including:
- Continuous real-time execution loop with persistent state management
- Custom multi-sign recording system with disk-based persistence
- Enhanced gesture recognition with configurable quality thresholds
- Offline text-to-speech integration (pyttsx3) for audio feedback
- Mode-switching architecture (Record/Recognize) for flexible operation
- Improved UI with real-time status display and keyboard controls
- Professional code structure, documentation, and error handling

## Core Technologies

Built with:
- **OpenCV** – Real-time video processing
- **MediaPipe** – Hand and pose landmark detection
- **Dynamic Time Warping (DTW)** – Gesture sequence comparison
- **NumPy** – Numerical computation
- **pyttsx3** – Offline text-to-speech synthesis

---

This acknowledgement reflects the collaborative nature of modern software development while maintaining honest attribution to both the AI assistant and the open-source community that inspired this work.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the project.

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Status:** Production-ready | **Version:** 2.0 | **Last Updated:** January 2026
