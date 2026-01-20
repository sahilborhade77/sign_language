import cv2
import mediapipe as mp
import sys

from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from utils.sign_storage import get_available_signs
from utils.voice_output import VoiceOutput
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager


# ============================================================================
# TODO: FUTURE ENHANCEMENTS
# ============================================================================
# 1. Static Alphabet Recognition
#    - Add a separate ML classifier for A-Z sign alphabet recognition
#    - Use with a dedicated model (e.g., CNN on hand landmarks)
#    - Can be triggered by a special key combination (e.g., 'a' for alphabet mode)
#
# 2. Speech-to-Sign
#    - Add speech recognition input (using speech_recognition library)
#    - Convert spoken words to corresponding signs
#    - Display animated sign sequences
# ============================================================================


def get_sign_name_input():
    """Get sign name from user input."""
    available_signs = get_available_signs()
    
    print("\n" + "="*60)
    print("📝 NEW SIGN RECORDING")
    print("="*60)
    
    if available_signs:
        print(f"\nExisting signs: {', '.join(available_signs)}")
    
    sign_name = input("\nEnter sign name (e.g., 'Hello', 'Thanks', 'Goodbye'): ").strip()
    
    if not sign_name:
        print("⚠ Sign name cannot be empty.")
        return None
    
    print(f"✓ Recording new sign: '{sign_name}'")
    return sign_name


def main():
    """Main application loop."""
    
    print("\n" + "="*60)
    print("🤟 SIGN LANGUAGE RECOGNITION SYSTEM v2.0")
    print("="*60)
    print("\nInitializing system...")
    
    # Load data
    videos = load_dataset()
    reference_signs = load_reference_signs(videos)
    
    # Initialize components
    sign_recorder = SignRecorder(reference_signs, mode="recognize")
    webcam_manager = WebcamManager()
    voice_output = VoiceOutput()
    
    # Current mode and sign name
    mode = "recognize"  # Start in recognize mode
    current_sign_name = None
    
    print("\n" + "="*60)
    print("KEYBOARD CONTROLS")
    print("="*60)
    print("  'r' = Start/Stop Recording")
    print("  'm' = Toggle Mode (RECORD ↔ RECOGNIZE)")
    print("  'n' = Record NEW Sign")
    print("  'q' = Quit")
    print("="*60)
    
    # Turn on the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("❌ ERROR: Cannot open webcam!")
        return
    
    print("\n✓ Webcam opened")
    print(f"✓ Starting in '{mode.upper()}' mode\n")
    
    # Set up the Mediapipe environment
    with mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        
        try:
            # ============================================================
            # MAIN CONTINUOUS LOOP
            # ============================================================
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Failed to read frame from webcam")
                    break

                # Make detections
                image, results = mediapipe_detection(frame, holistic)

                # Process results
                sign_detected, is_recording = sign_recorder.process_results(results)
                sequence_length = len(sign_recorder.recorded_results)

                # Update the frame (draw landmarks & display result)
                webcam_manager.update(
                    frame=image,
                    results=results,
                    sign_detected=sign_detected,
                    is_recording=is_recording,
                    sequence_length=sequence_length,
                    current_mode=mode,
                    current_sign_name=current_sign_name,
                    dtw_distance=sign_recorder.last_dtw_distance
                )

                # Handle keyboard input
                pressedKey = cv2.waitKey(1) & 0xFF
                
                if pressedKey == ord("r"):
                    # Toggle recording
                    if is_recording or sign_recorder.is_saving:
                        sign_recorder.stop_recording()
                        print("⏹ Recording stopped")
                    else:
                        if mode == "record":
                            if current_sign_name:
                                sign_recorder.record(current_sign_name)
                                print(f"🎥 Recording '{current_sign_name}'...")
                            else:
                                print("⚠ No sign name set. Press 'n' to record a new sign.")
                        else:
                            sign_recorder.record()
                            print("🎥 Recording gesture for recognition...")
                        
                elif pressedKey == ord("m"):
                    # Toggle mode
                    if mode == "record":
                        mode = "recognize"
                        current_sign_name = None
                    else:
                        mode = "record"
                    
                    sign_recorder.mode = mode
                    voice_output.reset()
                    print(f"\n✓ Switched to '{mode.upper()}' mode\n")
                    
                elif pressedKey == ord("n"):
                    # Record new sign
                    if mode != "record":
                        print("⚠ Switch to RECORD mode first (press 'm')")
                    else:
                        new_sign_name = get_sign_name_input()
                        if new_sign_name:
                            current_sign_name = new_sign_name
                            sign_recorder.record(current_sign_name)
                            print(f"🎥 Recording '{current_sign_name}'...")
                    
                elif pressedKey == ord("q"):
                    # Quit cleanly
                    print("\n🛑 Closing application...")
                    sign_recorder.stop_recording()
                    break
                
                # Speak recognized sign (only in recognize mode and when sign changes)
                if mode == "recognize" and sign_detected and not is_recording:
                    if sign_detected != "Unknown Sign" and sign_detected != "No reference signs":
                        voice_output.speak_sign(sign_detected)
        
        except KeyboardInterrupt:
            print("\n⚠ Interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            voice_output.cleanup()
            print("✓ Webcam released")
            print("✓ Windows closed")
            print("✓ Voice output cleaned up")
            print("\n✓ Program closed gracefully\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

