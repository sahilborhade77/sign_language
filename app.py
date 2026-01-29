import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import mediapipe as mp

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


def draw_text_pil(image, text):
    """Draw text using PIL (no OpenCV)"""
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, fill=(255, 0, 0))
    return np.array(img)


def main():
    st.set_page_config(page_title="Sign Language Recognition")

    st.title("🤟 Sign Language Recognition")
    st.markdown("Streamlit + MediaPipe based sign recognition")

    sign_recorder = load_sign_recorder()

    if "frames" not in st.session_state:
        st.session_state.frames = []
    if "recording" not in st.session_state:
        st.session_state.recording = False
    if "prediction" not in st.session_state:
        st.session_state.prediction = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎥 Start / Stop Recording"):
            st.session_state.recording = not st.session_state.recording
            st.session_state.frames = []

    with col2:
        if st.button("🔄 Reset"):
            st.session_state.frames = []
            st.session_state.prediction = None
            st.session_state.recording = False
            st.rerun()

    image_file = st.camera_input("Take a photo")

    if image_file:
        image = np.array(Image.open(image_file))

        with mp.solutions.holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as holistic:

            processed_image, results = mediapipe_detection(image, holistic)

            if st.session_state.recording:
                st.session_state.frames.append(results)
                st.info(f"Frames recorded: {len(st.session_state.frames)}")

                if len(st.session_state.frames) >= 40:
                    sign_recorder.recorded_results = st.session_state.frames
                    prediction = sign_recorder._compute_distances_and_predict()
                    st.session_state.prediction = prediction
                    st.session_state.frames = []
                    st.session_state.recording = False
            else:
                sign_recorder.recorded_results = [results]
                st.session_state.prediction = (
                    sign_recorder._compute_distances_and_predict()
                )

            annotated = draw_text_pil(
                processed_image,
                f"Prediction: {st.session_state.prediction or ''}"
            )

            st.image(annotated, caption="Processed Frame")

    signs = get_available_signs()
    if signs:
        with st.expander("📚 Available Signs"):
            for s in signs:
                st.write(f"• {s}")


if __name__ == "__main__":
    main()
