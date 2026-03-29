🤟 Sign Language Recognition System
A real-time sign language recognition system using computer vision and dynamic time warping for continuous gesture detection with voice output.


📌 Overview
This system performs real-time sign language recognition using a webcam. It captures hand landmarks via MediaPipe, compares gesture sequences using Dynamic Time Warping (DTW), and produces voice output — making it accessible for hearing-impaired communication.

✨ Features

Real-time hand tracking — MediaPipe hand landmark detection at 21 keypoints per hand
Custom sign recording — Record your own signs and add them to the recognition set
Continuous recognition — Recognizes signs in a live webcam stream without pause
Dynamic Time Warping (DTW) — Robust gesture matching that handles speed variation
Voice output — Text-to-speech output for recognized signs
Offline support — Works entirely offline, no internet needed


🛠 Tech Stack
ComponentTechnologyHand TrackingMediaPipeComputer VisionOpenCVGesture MatchingDynamic Time Warping (DTW)Voice Outputpyttsx3 (Text-to-Speech)LanguagePython 3.10

🧠 How It Works
Webcam Input
    │
    ▼
[MediaPipe] Hand Landmark Detection (21 keypoints)
    │
    ▼
[Preprocessing] Normalize & extract landmark sequences
    │
    ▼
[DTW Matching] Compare against stored sign templates
    │
    ▼
[Output] Display label + Voice announcement

📁 Project Structure
sign_language/
├── data/
│   └── signs/               # Stored sign gesture sequences (.npy)
├── modules/
│   ├── hand_tracker.py      # MediaPipe hand detection
│   ├── dtw_matcher.py       # DTW-based gesture matching
│   └── tts_output.py        # Text-to-speech output
├── record_sign.py           # Script to record new signs
├── recognize.py             # Real-time recognition script
├── requirements.txt
└── README.md

⚙️ Setup & Installation
Prerequisites

Python 3.10+
Webcam

Install Dependencies
bashgit clone https://github.com/sahilborhade77/sign_language.git
cd sign_language
pip install -r requirements.txt
Run Real-Time Recognition
bashpython recognize.py
Record a New Sign
bashpython record_sign.py --name "hello"

🚀 Usage

Run recognize.py to start the webcam
Perform a sign in front of the camera
The system displays the recognized label and announces it via voice
To add a new sign, run record_sign.py and follow the prompts


🔑 Key Technical Concepts

MediaPipe Hands — Detects 21 3D landmarks per hand in real time
DTW (Dynamic Time Warping) — Aligns gesture sequences of different lengths/speeds for robust matching
Landmark Normalization — Coordinates normalized relative to wrist position for scale/position invariance


🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.



👤 Author
Sahil Borhade
AI & ML Engineering Student, SPPU Pune
LinkedIn • GitHub
