"""
Module for text-to-speech output of recognized signs.
Uses pyttsx3 for offline speech synthesis.
"""

import pyttsx3
import threading


class VoiceOutput:
    """Handles text-to-speech for recognized signs."""
    
    def __init__(self, rate=150, volume=0.9):
        """
        Initialize TTS engine.
        
        :param rate: Speaking rate (words per minute)
        :param volume: Volume (0.0 to 1.0)
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        self.last_spoken = None
        print("✓ Voice output initialized")
    
    def speak_sign(self, sign_name):
        """
        Speak the sign name aloud (only if it's different from last spoken).
        Runs in a separate thread to avoid blocking the main loop.
        
        :param sign_name: Name of the sign to speak
        """
        # Only speak if it's a new sign (avoid repetition)
        if sign_name == self.last_spoken or sign_name in ["Unknown Sign", "No reference signs"]:
            return
        
        self.last_spoken = sign_name
        
        # Run speech in a background thread to avoid blocking
        thread = threading.Thread(target=self._speak_thread, args=(sign_name,))
        thread.daemon = True
        thread.start()
        
        print(f"🔊 Speaking: {sign_name}")
    
    def _speak_thread(self, text):
        """Internal method to speak text in a thread."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Voice output error: {e}")
    
    def reset(self):
        """Reset the last spoken sign (used when changing modes)."""
        self.last_spoken = None
    
    def cleanup(self):
        """Clean up TTS engine."""
        try:
            self.engine.stop()
        except:
            pass
