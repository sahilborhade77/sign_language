import streamlit as st
import numpy as np
from PIL import Image

from utils.mediapipe_utils import mediapipe_detection
from utils.sign_storage import get_available_signs
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager

# Cache model loading for performance and to avoid reloads
@st.cache_resource
def load_sign_recorder():
    """Load the sign recognition model once."""
    try:
        # Initialize with empty reference signs (will be populated by user recordings)
        return SignRecorder(reference_signs=None, mode="recognize")
    except Exception as e:
        st.error(f"Failed to load sign recorder: {e}")
        return None

@st.cache_resource
def load_webcam_mgr():
    """Load the webcam manager once."""
    return WebcamManager()

def main():
    st.title("🤟 Sign Language Recognition")
    st.markdown("Real-time sign language recognition using MediaPipe and DTW")

    # Load cached components
    sign_recorder = load_sign_recorder()
    webcam_manager = load_webcam_mgr()

    if sign_recorder is None:
        st.error("Failed to initialize sign recognition. Please refresh the page.")
        return

    # Initialize session state
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'recorded_frames' not in st.session_state:
        st.session_state.recorded_frames = []
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None

    # Minimal UI controls
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎥 Start/Stop Recording", type="primary"):
            if st.session_state.is_recording:
                st.session_state.is_recording = False
                st.session_state.recorded_frames = []
                st.success("Recording stopped")
            else:
                st.session_state.is_recording = True
                st.session_state.recorded_frames = []
                st.info("Recording started - take multiple photos")

    with col2:
        if st.button("🔄 Clear & Reset"):
            st.session_state.is_recording = False
            st.session_state.recorded_frames = []
            st.session_state.last_prediction = None
            sign_recorder.recorded_results = []
            st.rerun()

    # Camera input
    st.subheader("Camera Input")
    camera_image = st.camera_input("Take a photo")

    if camera_image is not None:
        # Convert to numpy array
        image = np.array(Image.open(camera_image))
        # PIL is RGB, keep as RGB for MediaPipe
        image_rgb = image

        # Process with MediaPipe
        import mediapipe as mp
        with mp.solutions.holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1  # CPU optimized
        ) as holistic:

            processed_image, results = mediapipe_detection(image_rgb, holistic)

            # Handle recording or recognition
            if st.session_state.is_recording:
                # Add frame to recording buffer
                st.session_state.recorded_frames.append(results)
                st.info(f"Frame recorded ({len(st.session_state.recorded_frames)}/50)")

                # Auto-stop when enough frames collected
                if len(st.session_state.recorded_frames) >= 50:
                    sign_recorder.recorded_results = st.session_state.recorded_frames
                    prediction = sign_recorder._compute_distances_and_predict()
                    st.session_state.last_prediction = prediction
                    st.session_state.is_recording = False
                    st.session_state.recorded_frames = []
                    st.success(f"Recording complete! Predicted: **{prediction}**")

            else:
                # Single frame recognition
                sign_recorder.recorded_results = [results]
                prediction = sign_recorder._compute_distances_and_predict()
                st.session_state.last_prediction = prediction

            # Display processed image with landmarks
            display_image = webcam_manager.draw_landmarks_on_image(processed_image.copy(), results)
            display_image = webcam_manager.add_text_overlay(
                display_image,
                sign_detected=st.session_state.last_prediction or "",
                is_recording=st.session_state.is_recording,
                sequence_length=len(st.session_state.recorded_frames),
                current_mode="recognize",
                current_sign_name="",
                dtw_distance=sign_recorder.last_dtw_distance
            )

            st.image(display_image, caption="Processed Frame")

            # Show prediction
            if st.session_state.last_prediction:
                st.success(f"🎯 Prediction: **{st.session_state.last_prediction}**")

    # Show available signs
    available_signs = get_available_signs()
    if available_signs:
        with st.expander("Available Signs"):
            for sign in available_signs:
                st.write(f"• {sign}")
    else:
        st.info("No signs recorded yet. Start recording to create reference signs!")

if __name__ == "__main__":
    main()
