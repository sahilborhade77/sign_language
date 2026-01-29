import pyttsx3

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.last_spoken = None

    def speak_sign(self, sign_name):
        """
        Speak the recognized sign name.
        
        :param sign_name: Name of the sign to speak
        """
        if sign_name != self.last_spoken:
            self.engine.say(sign_name)
            self.engine.runAndWait()
            self.last_spoken = sign_name

    def reset(self):
        """Reset the last spoken sign."""
        self.last_spoken = None

    def cleanup(self):
        """Cleanup the voice engine."""
        self.engine.stop()
