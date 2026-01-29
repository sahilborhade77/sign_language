from PIL import Image, ImageDraw, ImageFont
import numpy as np

WHITE_COLOR = (245, 242, 226)
RED_COLOR = (25, 35, 240)
GREEN_COLOR = (25, 200, 25)
YELLOW_COLOR = (25, 200, 200)
CYAN_COLOR = (200, 200, 25)

HEIGHT = 600


def safe_text(text):
    """Convert any text to ASCII-safe string for PIL."""
    if text is None:
        return ""
    return str(text).encode("ascii", "ignore").decode("ascii")


class WebcamManager(object):
    """Adds text overlays using PIL (Unicode-safe, Streamlit Cloud safe)."""

    def __init__(self):
        try:
            self.font = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            self.font = ImageFont.load_default()

    def draw_landmarks_on_image(self, image: np.ndarray, results):
        return image

    def add_text_overlay(
        self,
        image: np.ndarray,
        sign_detected: str,
        is_recording: bool,
        sequence_length: int = 0,
        current_mode: str = "recognize",
        current_sign_name: str = "",
        dtw_distance: float = None,
    ):
        pil_image = Image.fromarray(image)

        w, h = pil_image.size
        aspect_ratio = w / h
        new_w = int(HEIGHT * aspect_ratio)
        pil_image = pil_image.resize((new_w, HEIGHT), Image.Resampling.LANCZOS)
        pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)

        draw = ImageDraw.Draw(pil_image)

        # Mode
        mode_text = safe_text(f"MODE: {current_mode.upper()}")
        mode_color = RED_COLOR if current_mode == "record" else GREEN_COLOR
        draw.text((10, 10), mode_text, fill=mode_color, font=self.font)

        # Recording status
        if is_recording:
            status_text = safe_text(f"Recording ({sequence_length}/50 frames)")
            draw.text((10, 40), status_text, fill=RED_COLOR, font=self.font)

        # Sign name
        if current_sign_name and current_mode == "record":
            sign_name_text = safe_text(f"Sign: {current_sign_name}")
            draw.text((10, 70), sign_name_text, fill=YELLOW_COLOR, font=self.font)

        # DTW distance
        if dtw_distance is not None:
            distance_text = safe_text(f"DTW Distance: {dtw_distance:.2f}")
            draw.text((10, 100), distance_text, fill=CYAN_COLOR, font=self.font)

        # Prediction (bottom)
        if sign_detected:
            self.draw_text(pil_image, safe_text(sign_detected), draw)

        # Status indicator
        indicator_color = RED_COLOR if is_recording else WHITE_COLOR
        draw.ellipse([new_w - 45, 15, new_w - 15, 45], fill=indicator_color)

        return np.array(pil_image)

    def draw_text(
        self,
        pil_image,
        text,
        draw=None,
        offset=int(HEIGHT * 0.02),
        bg_color=(245, 242, 176),
        text_color=(118, 62, 37),
    ):
        if draw is None:
            draw = ImageDraw.Draw(pil_image)

        text = safe_text(text)

        w, h = pil_image.size
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        text_x = int((w - text_w) / 2)
        text_y = h - text_h - offset

        draw.rectangle([0, text_y - offset, w, h], fill=bg_color)
        draw.text((text_x, text_y), text, fill=text_color, font=self.font)

        return pil_image
