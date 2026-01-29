# ---------- IMPORTANT: must come BEFORE cv2 ----------
import os
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"
# ----------------------------------------------------

import streamlit as st
import numpy as np
from PIL import Image

# Lazy import cv2 (safe for Streamlit Cloud)
import cv2
import mediapipe as mp

from utils.mediapipe_utils import mediapipe_detection
from utils.sign_storage import get_available_signs
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager


# Cache model loading for performance and to avoid reloads
@st.cache_resource
def load_sign_recorder():
    """Load the sign recognition model once."""
    return SignRecorder(reference_signs=None, mode="recognize")


@st.cache_resource
def load_webcam_mgr():
    """Load the webcam manager once."""
    return WebcamManager()


def main():
    st.set_page_config(
        page_title="Sign Language Recognition",
        layout="centered"
    )

    st.title("🤟 Sign Language Recognition")
    st.markdown("Snapshot-based sign language recognition using MediaPipe and DTW")

    # Load cached components
    sign_recorder = load_sign_recorder()
    webcam_manager = load_webcam_mgr()

    # Initialize session state
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False
    if "recorded_frames" not in st.session_state:
        st.session_state.recorded_frames = []
    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = None

    # Controls
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎥 Start / Stop Recording", type="primary"):
            st.session_state.is_recording = not st.session_state.is_recording
            if st.session_state.is_recording:
                st.session_state.recorded_frames = []
                st.info("Recording started — take multiple photos")
            else:
                st.success("Recording stopped")

    with col2:
        if st.button("🔄 Reset"):
            st.session_state.is_recording = False
            st.session_state.recorded_frames = []
            st.session_state.last_prediction = None
            sign_recorder.recorded_results = []
            st.rerun()

    # Camera input (Streamlit-safe)
    st.subheader("📷 Camera Input")
    camera_image = st.camera_input("Capture frame")

    if camera_image is not None:
        # Convert to OpenCV format
        image = np.array(Image.open(camera_image))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # MediaPipe processing
        with mp.solutions.holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        ) as holistic:

            processed_image, results = mediapipe_detection(image, holistic)

            # Recording mode
            if st.session_state.is_recording:
                st.session_state.recorded_frames.append(results)
                st.info(f"Frames recorded: {len(st.session_state.recorded_frames)}/50")

                if len(st.session_state.recorded_frames) >= 50:
                    sign_recorder.recorded_results = st.session_state.recorded_frames
                    prediction = sign_recorder._compute_distances_and_predict()
                    st.session_state.last_prediction = prediction
                    st.session_state.is_recording = False
                    st.session_state.recorded_frames = []
                    st.success(f"✅ Prediction: **{prediction}**")

            # Single-frame inference
            else:
                sign_recorder.recorded_results = [results]
                prediction = sign_recorder._compute_distances_and_predict()
                st.session_state.last_prediction = prediction

            # Draw landmarks
            display_image = webcam_manager.draw_landmarks_on_image(
                processed_image.copy(), results
            )

            display_image = webcam_manager.add_text_overlay(
                display_image,
                sign_detected=st.session_state.last_prediction or "",
                is_recording=st.session_state.is_recording,
                sequence_length=len(st.session_state.recorded_frames),
                current_mode="recognize",
                current_sign_name=None,
                dtw_distance=sign_recorder.last_dtw_distance,
            )

            st.image(display_image, channels="BGR", caption="Processed Frame")

            if st.session_state.last_prediction:
                st.success(f"🎯 Prediction: **{st.session_state.last_prediction}**")

    # Available signs
    available_signs = get_available_signs()
    if available_signs:
        with st.expander("📚 Available Signs"):
            for sign in available_signs:
                st.write(f"• {sign}")
    else:
        st.info("No reference signs found yet.")


if __name__ == "__main__":
    main()
