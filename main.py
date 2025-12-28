#!/usr/bin/env python3
"""
Hi-Tech Interactive Robot - Main Controller
Author: Rakesh Behera
Description: Main entry point for the interactive robot system
"""

import sys
import time
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.speech.speech_recognizer import SpeechRecognizer
from src.speech.text_to_speech import TextToSpeech
from src.gesture.gesture_controller import GestureController
from src.vision.vision_processor import VisionProcessor
from src.hardware.servo_controller import ServoController
from src.hardware.led_controller import LEDController
from src.ai.brain import RobotBrain
from config.config_loader import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('robot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InteractiveRobot:
    """Main robot controller class"""
    
    def __init__(self):
        """Initialize robot components"""
        logger.info("Initializing Hi-Tech Interactive Robot...")
        
        # Load configuration
        self.config = load_config()
        
        # Initialize components
        self.speech_recognizer = SpeechRecognizer(self.config)
        self.tts = TextToSpeech(self.config)
        self.gesture_controller = GestureController(self.config)
        self.vision_processor = VisionProcessor(self.config)
        self.servo_controller = ServoController(self.config)
        self.led_controller = LEDController(self.config)
        self.brain = RobotBrain(self.config)
        
        self.is_running = False
        logger.info("Robot initialized successfully!")
        
    def start(self):
        """Start the robot"""
        logger.info("Starting robot...")
        self.is_running = True
        
        # Welcome message
        self.tts.speak("Hello! I am your interactive robot. How can I help you today?")
        self.led_controller.set_expression("happy")
        
        try:
            self.main_loop()
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
            self.shutdown()
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
            self.shutdown()
    
    def main_loop(self):
        """Main robot control loop"""
        while self.is_running:
            try:
                # Listen for voice commands
                logger.info("Listening for commands...")
                self.led_controller.set_expression("listening")
                
                command = self.speech_recognizer.listen()
                
                if command:
                    logger.info(f"Received command: {command}")
                    self.process_command(command)
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in main loop iteration: {e}")
                time.sleep(1)
    
    def process_command(self, command):
        """Process voice command"""
        # Process through AI brain
        response = self.brain.process(command)
        
        # Execute actions based on response
        if response.get('action'):
            self.execute_action(response['action'], response.get('parameters', {}))
        
        # Speak response
        if response.get('speech'):
            self.tts.speak(response['speech'])
        
        # Update LED expression
        if response.get('expression'):
            self.led_controller.set_expression(response['expression'])
    
    def execute_action(self, action, parameters):
        """Execute robot action"""
        logger.info(f"Executing action: {action}")
        
        actions = {
            'wave': lambda: self.gesture_controller.wave(),
            'nod': lambda: self.gesture_controller.nod(),
            'shake_head': lambda: self.gesture_controller.shake_head(),
            'point': lambda: self.gesture_controller.point(parameters.get('direction')),
            'dance': lambda: self.gesture_controller.dance(),
            'look_around': lambda: self.gesture_controller.look_around(),
            'greet': lambda: self.gesture_controller.greet(),
            'thumbs_up': lambda: self.gesture_controller.thumbs_up(),
            'take_photo': lambda: self.vision_processor.capture_image(),
            'detect_face': lambda: self.vision_processor.detect_faces(),
            'track_object': lambda: self.vision_processor.track_object(parameters.get('object')),
        }
        
        if action in actions:
            actions[action]()
        else:
            logger.warning(f"Unknown action: {action}")
    
    def shutdown(self):
        """Shutdown robot gracefully"""
        logger.info("Shutting down robot...")
        self.is_running = False
        
        self.tts.speak("Goodbye! Shutting down now.")
        self.led_controller.set_expression("sleep")
        
        # Cleanup
        self.servo_controller.reset_position()
        self.led_controller.turn_off()
        self.vision_processor.cleanup()
        
        logger.info("Robot shutdown complete")


def main():
    """Main entry point"""
    print("=" * 50)
    print("Hi-Tech Interactive Robot System")
    print("=" * 50)
    
    robot = InteractiveRobot()
    robot.start()


if __name__ == "__main__":
    main()
