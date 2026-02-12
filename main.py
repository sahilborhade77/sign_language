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
# SIGN LANGUAGE RECOGNITION SYSTEM v3.0
# ============================================================================
# Key Improvements:
# 1. Distance-invariant landmarks (normalized by wrist + hand size)
# 2. Gesture-based recording (open palm → record, fist → stop)
# 3. Stability-based prediction (10+ frames confirmation)
# 4. Sentence buffer (accumulate words instead of single word)
# 5. Comprehensive visual feedback (confidence, status, frame count)
# 6. Idle state handling (detect absence of hands)
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
    """Main application loop with gesture-based control."""
    
    print("\n" + "="*60)
    print("🤟 SIGN LANGUAGE RECOGNITION SYSTEM v3.0")
    print("="*60)
    print("\nInitializing system...")
    
    # Load data
    videos = load_dataset()
    reference_signs = load_reference_signs(videos)
    
    # Initialize components
    sign_recorder = SignRecorder(reference_signs, mode="recognize")
    webcam_manager = WebcamManager()
    voice_output = VoiceOutput()
    
    # Current mode and state
    mode = "recognize"  # Start in recognize mode
    current_sign_name = None
    
    # ===== NEW: Sentence buffer for accumulating words =====
    sentence_buffer = []  # List of recognized signs
    last_spoken_sign = None  # Track which sign we last spoke
    
    print("\n" + "="*60)
    print("GESTURE-BASED CONTROLS (NO KEYBOARD NEEDED!)")
    print("="*60)
    print("  OPEN PALM  → Start Recording")
    print("  FIST       → Stop Recording & Recognize")
    print("  PRESS 'm'  → Toggle Record/Recognize Mode")
    print("  PRESS 'n'  → Record New Sign (Record Mode)")
    print("  PRESS 'c'  → Clear Sentence Buffer")
    print("  PRESS 'q'  → Quit")
    print("="*60)
    print("\n✓ System Ready - Begin signing!\n")
    
    # Turn on the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("❌ ERROR: Cannot open webcam!")
        return
    
    print("\n✓ Webcam opened")
    print(f"✓ Starting in '{mode.upper()}' mode\n")
    
    # Set up the Mediapipe environment
    with mp.solutions.holistic.Holistic(  # type: ignore
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

                # ===== NEW: Process results with new return format =====
                sign_detected, is_recording, status = sign_recorder.process_results(results)
                sequence_length = status['frame_count']
                hand_visible = status['hand_visible']

                # Update the frame with enhanced visual feedback
                webcam_manager.update(
                    frame=image,
                    results=results,
                    sign_detected=sign_detected,
                    sentence_buffer=sentence_buffer,  # NEW: Show full sentence
                    is_recording=is_recording,
                    sequence_length=sequence_length,
                    hand_visible=hand_visible,  # NEW: Show idle status
                    current_mode=mode,
                    current_sign_name=current_sign_name,
                    dtw_distance=sign_recorder.last_dtw_distance,
                    confidence=status['confidence']  # NEW: Show confidence
                )
                
                # ===== NEW: Handle recognized signs (add to sentence buffer) =====
                if sign_detected and sign_detected not in ["Unknown Sign", "No reference signs", ""]:
                    if sign_detected != last_spoken_sign:
                        # Add to sentence buffer
                        sentence_buffer.append(sign_detected)
                        
                        # Speak the word
                        voice_output.speak_sign(sign_detected)
                        last_spoken_sign = sign_detected
                        
                        print(f"✓ Sign added to sentence: {' '.join(sentence_buffer)}")
                
                # Handle "Unknown Sign" feedback
                if sign_detected == "Unknown Sign":
                    if last_spoken_sign != "Unknown Sign":
                        voice_output.speak_unknown()
                        last_spoken_sign = "Unknown Sign"

                # Handle keyboard input
                pressedKey = cv2.waitKey(1) & 0xFF
                
                # ===== REMOVED: 'r' key recording (now gesture-based) =====
                # Gesture detection is automatic via open palm/fist
                
                if pressedKey == ord("m"):
                    # Toggle mode
                    if mode == "record":
                        mode = "recognize"
                        current_sign_name = None
                    else:
                        mode = "record"
                    
                    sign_recorder.mode = mode
                    voice_output.reset()
                    last_spoken_sign = None  # Reset voice tracking when switching modes
                    print(f"\n✓ Switched to '{mode.upper()}' mode\n")
                
                elif pressedKey == ord("c"):
                    # ===== NEW: Clear sentence buffer =====
                    sentence_buffer = []
                    last_spoken_sign = None
                    print("\n🗑️  Sentence buffer cleared\n")
                    
                elif pressedKey == ord("n"):
                    # Record new sign
                    if mode != "record":
                        print("⚠ Switch to RECORD mode first (press 'm')")
                    else:
                        new_sign_name = get_sign_name_input()
                        if new_sign_name:
                            current_sign_name = new_sign_name
                            sign_recorder.record(current_sign_name)
                            print(f"🎥 Recording '{current_sign_name}'...\n")
                    
                elif pressedKey == ord("q"):
                    # Quit cleanly
                    print("\n🛑 Closing application...")
                    sign_recorder.stop_recording()
                    break
        
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
