import streamlit as st
import numpy as np
from PIL import Image

from utils.mediapipe_utils import mediapipe_detection
from utils.sign_storage import get_available_signs
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager


@st.cache_resource
def load_sign_recorder():
    return SignRecorder(reference_signs=None, mode="recognize")


@st.cache_resource
def load_webcam_mgr():
    return WebcamManager()


def main():
    st.title("🤟 Sign Language Recognition")
    st.markdown("Sign language recognition using MediaPipe and DTW")

    sign_recorder = load_sign_recorder()
    webcam_manager = load_webcam_mgr()

    # ---------- Session State ----------
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False
    if "recorded_frames" not in st.session_state:
        st.session_state.recorded_frames = []
    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = None
    if "current_sign_name" not in st.session_state:
        st.session_state.current_sign_name = ""

    # ---------- Sign Name Input ----------
    st.subheader("📝 Record New Sign")
    st.session_state.current_sign_name = st.text_input(
        "Enter sign name (e.g. HELLO, THANK_YOU)",
        value=st.session_state.current_sign_name
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎥 Start Recording", type="primary"):
            if not st.session_state.current_sign_name.strip():
                st.warning("Please enter a sign name before recording.")
            else:
                st.session_state.is_recording = True
                st.session_state.recorded_frames = []
                st.info(f"Recording sign: {st.session_state.current_sign_name}")

    with col2:
        if st.button("⏹ Stop Recording"):
            st.session_state.is_recording = False
            st.success("Recording stopped")

    with col3:
        if st.button("🔄 Reset"):
            st.session_state.is_recording = False
            st.session_state.recorded_frames = []
            st.session_state.last_prediction = None
            sign_recorder.recorded_results = []
            st.rerun()

    # ---------- Camera Input ----------
    st.subheader("📷 Camera Input")
    camera_image = st.camera_input("Take a photo")

    if camera_image is not None:
        image = np.array(Image.open(camera_image))
        image_rgb = image  # MediaPipe expects RGB

        processed_image, results = mediapipe_detection(image_rgb)

        if st.session_state.is_recording:
            st.session_state.recorded_frames.append(results)
            st.info(f"Frames recorded: {len(st.session_state.recorded_frames)}/50")

            if len(st.session_state.recorded_frames) >= 50:
                sign_recorder.recorded_results = st.session_state.recorded_frames
                sign_recorder.save_reference_sign(
                    st.session_state.current_sign_name
                )
                st.success(f"Saved sign: {st.session_state.current_sign_name}")
                st.session_state.is_recording = False
                st.session_state.recorded_frames = []

        else:
            sign_recorder.recorded_results = [results]
            prediction = sign_recorder._compute_distances_and_predict()
            st.session_state.last_prediction = prediction

        display_image = webcam_manager.add_text_overlay(
            processed_image.copy(),
            sign_detected=st.session_state.last_prediction or "",
            is_recording=st.session_state.is_recording,
            sequence_length=len(st.session_state.recorded_frames),
            current_mode="record" if st.session_state.is_recording else "recognize",
            current_sign_name=st.session_state.current_sign_name,
            dtw_distance=sign_recorder.last_dtw_distance
        )

        st.image(display_image, caption="Processed Frame")

        if st.session_state.last_prediction:
            st.success(f"🎯 Prediction: **{st.session_state.last_prediction}**")

    # ---------- Available Signs ----------
    available_signs = get_available_signs()
    if available_signs:
        with st.expander("📁 Available Signs"):
            for sign in available_signs:
                st.write(f"• {sign}")
    else:
        st.info("No signs recorded yet.")

if __name__ == "__main__":
    main()
