"""
Text-to-Speech Module
Converts text to natural speech output
"""

import pyttsx3
import logging
from typing import Optional
import threading

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Text-to-speech handler"""
    
    def __init__(self, config):
        """Initialize TTS engine"""
        self.config = config
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        voices = self.engine.getProperty('voices')
        voice_id = config.get('tts', {}).get('voice_id', 0)
        
        if voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)
        
        # Set speech rate and volume
        rate = config.get('tts', {}).get('rate', 150)
        volume = config.get('tts', {}).get('volume', 1.0)
        
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        self.is_speaking = False
        logger.info("TTS engine initialized")
    
    def speak(self, text: str, blocking: bool = True):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            blocking: Wait for speech to complete
        """
        if not text:
            return
        
        logger.info(f"Speaking: {text}")
        self.is_speaking = True
        
        try:
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Non-blocking speech
                thread = threading.Thread(target=self._speak_async, args=(text,))
                thread.daemon = True
                thread.start()
        except Exception as e:
            logger.error(f"TTS error: {e}")
        finally:
            self.is_speaking = False
    
    def _speak_async(self, text: str):
        """Async speech helper"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Async TTS error: {e}")
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
            self.is_speaking = False
            logger.info("Speech stopped")
        except Exception as e:
            logger.error(f"Error stopping speech: {e}")
    
    def set_rate(self, rate: int):
        """
        Set speech rate
        
        Args:
            rate: Words per minute (50-300)
        """
        self.engine.setProperty('rate', rate)
        logger.info(f"Speech rate set to {rate}")
    
    def set_volume(self, volume: float):
        """
        Set speech volume
        
        Args:
            volume: Volume level (0.0-1.0)
        """
        self.engine.setProperty('volume', volume)
        logger.info(f"Volume set to {volume}")
    
    def list_voices(self):
        """List available voices"""
        voices = self.engine.getProperty('voices')
        for idx, voice in enumerate(voices):
            logger.info(f"Voice {idx}: {voice.name} - {voice.languages}")
        return voices
