from PIL import Image, ImageDraw, ImageFont
import numpy as np

WHITE_COLOR = (245, 242, 226)
RED_COLOR = (25, 35, 240)
GREEN_COLOR = (25, 200, 25)
YELLOW_COLOR = (25, 200, 200)
CYAN_COLOR = (200, 200, 25)

HEIGHT = 600

class WebcamManager(object):
    """Object that adds text overlays to images for Streamlit display using PIL"""

    def __init__(self):
        self.sign_detected = ""
        # Load default font
        try:
            self.font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            self.font = ImageFont.load_default()

    def draw_landmarks_on_image(self, image: np.ndarray, results):
        """
        Return the image without drawing landmarks (removed to avoid cv2 dependency).

        :param image: Input image
        :param results: MediaPipe detection results (unused)
        :return: Original image
        """
        # Landmarks drawing removed to avoid MediaPipe drawing_utils (uses cv2)
        return image

    def add_text_overlay(
        self, image: np.ndarray, sign_detected: str, is_recording: bool,
        sequence_length: int = 0, current_mode: str = "recognize", current_sign_name: str = "",
        dtw_distance: float = None
    ):
        """
        Add text overlay to the image using PIL.

        :param image: Input image (numpy array)
        :param sign_detected: Detected sign name
        :param is_recording: Whether currently recording
        :param sequence_length: Number of frames collected
        :param current_mode: Current mode ("record" or "recognize")
        :param current_sign_name: Name of sign being recorded
        :param dtw_distance: DTW distance for debugging
        :return: Image with text overlay (PIL Image)
        """
        self.sign_detected = sign_detected

        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(image)

        # Resize frame
        h, w = pil_image.size[::-1]  # PIL size is (w, h)
        aspect_ratio = w / h
        new_w = int(HEIGHT * aspect_ratio)
        pil_image = pil_image.resize((new_w, HEIGHT), Image.ANTIALIAS)

        # Flip the image horizontally for mirror effect
        pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)

        # Create draw object
        draw = ImageDraw.Draw(pil_image)

        # Draw mode indicator
        mode_text = f"MODE: {current_mode.upper()}"
        mode_color = RED_COLOR if current_mode == "record" else GREEN_COLOR
        draw.text((10, 10), mode_text, fill=mode_color, font=self.font)

        # Draw recording status message
        if is_recording:
            status_text = f"🎥 Recording... ({sequence_length}/50 frames)"
            draw.text((10, 40), status_text, fill=RED_COLOR, font=self.font)

        # Draw current sign name being recorded
        if current_sign_name and current_mode == "record":
            sign_name_text = f"Sign: '{current_sign_name}'"
            draw.text((10, 70), sign_name_text, fill=YELLOW_COLOR, font=self.font)

        # Draw DTW distance (for debugging)
        if dtw_distance is not None:
            distance_text = f"DTW Distance: {dtw_distance:.2f}"
            draw.text((10, 100), distance_text, fill=CYAN_COLOR, font=self.font)

        # Draw detected sign
        if sign_detected:
            pil_image = self.draw_text(pil_image, sign_detected, draw)

        # Status circle color
        color = WHITE_COLOR
        if is_recording:
            color = RED_COLOR

        # Draw status indicator (circle)
        draw.ellipse([new_w - 45, 15, new_w - 15, 45], fill=color)

        # Convert back to numpy array for Streamlit
        return np.array(pil_image)

    def draw_text(
        self,
        pil_image,
        text,
        draw=None,
        offset=int(HEIGHT * 0.02),
        bg_color=(245, 242, 176),
        text_color=(118, 62, 37)
    ):
        if draw is None:
            draw = ImageDraw.Draw(pil_image)

        w, h = pil_image.size

        # Estimate text size (PIL doesn't have getTextSize like cv2)
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        text_x = int((w - text_w) / 2)
        text_y = h - text_h - offset

        # Draw background rectangle
        draw.rectangle([0, text_y - offset, w, h], fill=bg_color)

        # Draw text
        draw.text((text_x, text_y), text, fill=text_color, font=self.font)

        return pil_image
