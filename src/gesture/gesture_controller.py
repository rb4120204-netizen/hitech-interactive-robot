"""
Gesture Controller Module
Controls robot physical movements and gestures
"""

import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class GestureController:
    """Handles robot gestures and movements"""
    
    def __init__(self, config):
        """Initialize gesture controller"""
        self.config = config
        
        # Import servo controller
        from src.hardware.servo_controller import ServoController
        self.servo = ServoController(config)
        
        # Gesture definitions
        self.gestures = self._load_gestures()
        logger.info("Gesture controller initialized")
    
    def _load_gestures(self) -> Dict:
        """Load predefined gestures"""
        return {
            'wave': [
                {'servo': 'right_shoulder', 'angle': 90, 'speed': 0.5},
                {'servo': 'right_elbow', 'angle': 45, 'speed': 0.5},
                {'servo': 'right_wrist', 'angle': 0, 'speed': 0.3, 'repeat': 3},
            ],
            'nod': [
                {'servo': 'head_tilt', 'angle': 20, 'speed': 0.3},
                {'servo': 'head_tilt', 'angle': -10, 'speed': 0.3, 'repeat': 2},
            ],
            'shake_head': [
                {'servo': 'head_pan', 'angle': 30, 'speed': 0.4},
                {'servo': 'head_pan', 'angle': -30, 'speed': 0.4, 'repeat': 2},
            ],
            'thumbs_up': [
                {'servo': 'right_shoulder', 'angle': 45, 'speed': 0.5},
                {'servo': 'right_elbow', 'angle': 90, 'speed': 0.5},
                {'servo': 'right_thumb', 'angle': 90, 'speed': 0.3},
            ],
            'point': [
                {'servo': 'right_shoulder', 'angle': 60, 'speed': 0.5},
                {'servo': 'right_elbow', 'angle': 180, 'speed': 0.5},
                {'servo': 'right_index', 'angle': 180, 'speed': 0.3},
            ],
        }
    
    def wave(self):
        """Perform waving gesture"""
        logger.info("Performing wave gesture")
        self._execute_gesture('wave')
        self.servo.reset_position()
    
    def nod(self):
        """Perform nodding gesture"""
        logger.info("Performing nod gesture")
        self._execute_gesture('nod')
        self.servo.reset_position()
    
    def shake_head(self):
        """Perform head shaking gesture"""
        logger.info("Performing shake head gesture")
        self._execute_gesture('shake_head')
        self.servo.reset_position()
    
    def thumbs_up(self):
        """Perform thumbs up gesture"""
        logger.info("Performing thumbs up gesture")
        self._execute_gesture('thumbs_up')
        time.sleep(2)
        self.servo.reset_position()
    
    def point(self, direction: str = 'forward'):
        """
        Point in a direction
        
        Args:
            direction: Direction to point (forward, left, right, up, down)
        """
        logger.info(f"Pointing {direction}")
        
        direction_angles = {
            'forward': {'head_pan': 0, 'right_shoulder': 60},
            'left': {'head_pan': -45, 'right_shoulder': 90},
            'right': {'head_pan': 45, 'right_shoulder': 30},
            'up': {'head_tilt': -30, 'right_shoulder': 30},
            'down': {'head_tilt': 30, 'right_shoulder': 90},
        }
        
        angles = direction_angles.get(direction, direction_angles['forward'])
        
        for servo_name, angle in angles.items():
            self.servo.move_servo(servo_name, angle)
        
        self._execute_gesture('point')
        time.sleep(2)
        self.servo.reset_position()
    
    def greet(self):
        """Perform greeting gesture"""
        logger.info("Performing greeting")
        self.wave()
        time.sleep(0.5)
        self.nod()
    
    def dance(self):
        """Perform dance moves"""
        logger.info("Performing dance")
        
        dance_moves = [
            {'servo': 'left_shoulder', 'angle': 90, 'speed': 0.3},
            {'servo': 'right_shoulder', 'angle': 90, 'speed': 0.3},
            {'servo': 'left_shoulder', 'angle': 0, 'speed': 0.3},
            {'servo': 'right_shoulder', 'angle': 0, 'speed': 0.3},
            {'servo': 'head_pan', 'angle': 30, 'speed': 0.2},
            {'servo': 'head_pan', 'angle': -30, 'speed': 0.2},
        ]
        
        for _ in range(3):
            for move in dance_moves:
                self.servo.move_servo(
                    move['servo'],
                    move['angle'],
                    move.get('speed', 0.5)
                )
                time.sleep(0.2)
        
        self.servo.reset_position()
    
    def look_around(self):
        """Look around by moving head"""
        logger.info("Looking around")
        
        positions = [
            {'head_pan': 45, 'head_tilt': 0},
            {'head_pan': 45, 'head_tilt': -20},
            {'head_pan': 0, 'head_tilt': -20},
            {'head_pan': -45, 'head_tilt': -20},
            {'head_pan': -45, 'head_tilt': 0},
            {'head_pan': 0, 'head_tilt': 0},
        ]
        
        for pos in positions:
            for servo_name, angle in pos.items():
                self.servo.move_servo(servo_name, angle, speed=0.4)
            time.sleep(0.8)
        
        self.servo.reset_position()
    
    def _execute_gesture(self, gesture_name: str):
        """Execute a predefined gesture"""
        if gesture_name not in self.gestures:
            logger.warning(f"Unknown gesture: {gesture_name}")
            return
        
        gesture_sequence = self.gestures[gesture_name]
        
        for move in gesture_sequence:
            repeats = move.get('repeat', 1)
            
            for _ in range(repeats):
                self.servo.move_servo(
                    move['servo'],
                    move['angle'],
                    move.get('speed', 0.5)
                )
                time.sleep(0.3)
    
    def custom_gesture(self, moves: List[Dict]):
        """
        Execute custom gesture sequence
        
        Args:
            moves: List of move dictionaries with servo, angle, speed
        """
        logger.info("Executing custom gesture")
        
        for move in moves:
            self.servo.move_servo(
                move['servo'],
                move['angle'],
                move.get('speed', 0.5)
            )
            time.sleep(move.get('delay', 0.3))
        
        self.servo.reset_position()
