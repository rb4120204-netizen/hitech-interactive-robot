"""
Speech Recognition Module
Handles voice input and converts speech to text
"""

import speech_recognition as sr
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """Speech recognition handler"""
    
    def __init__(self, config):
        """Initialize speech recognizer"""
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        # Configuration
        self.language = config.get('speech', {}).get('language', 'en-US')
        self.timeout = config.get('speech', {}).get('timeout', 5)
        self.phrase_time_limit = config.get('speech', {}).get('phrase_time_limit', 10)
        
        logger.info("Speech recognizer initialized")
    
    def listen(self) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Returns:
            str: Recognized text or None if no speech detected
        """
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )
            
            logger.info("Processing speech...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            logger.debug("No speech detected (timeout)")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None
    
    def listen_continuous(self, callback):
        """
        Continuous listening mode
        
        Args:
            callback: Function to call with recognized text
        """
        def audio_callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio, language=self.language)
                callback(text.lower())
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                logger.error(f"Recognition error: {e}")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            audio_callback
        )
        
        return stop_listening
    
    def set_sensitivity(self, energy_threshold: int):
        """
        Adjust microphone sensitivity
        
        Args:
            energy_threshold: Energy level threshold (300-4000)
        """
        self.recognizer.energy_threshold = energy_threshold
        logger.info(f"Sensitivity set to {energy_threshold}")
