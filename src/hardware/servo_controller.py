"""
Servo Controller Module
Controls servo motors via Arduino/PCA9685
"""

import serial
import time
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ServoController:
    """Servo motor controller"""
    
    def __init__(self, config):
        """Initialize servo controller"""
        self.config = config
        
        # Servo configuration
        self.servos = {
            'head_pan': {'pin': 0, 'min': 0, 'max': 180, 'default': 90},
            'head_tilt': {'pin': 1, 'min': 0, 'max': 180, 'default': 90},
            'right_shoulder': {'pin': 2, 'min': 0, 'max': 180, 'default': 45},
            'right_elbow': {'pin': 3, 'min': 0, 'max': 180, 'default': 90},
            'right_wrist': {'pin': 4, 'min': 0, 'max': 180, 'default': 90},
            'right_thumb': {'pin': 5, 'min': 0, 'max': 90, 'default': 0},
            'right_index': {'pin': 6, 'min': 0, 'max': 180, 'default': 0},
            'left_shoulder': {'pin': 7, 'min': 0, 'max': 180, 'default': 45},
            'left_elbow': {'pin': 8, 'min': 0, 'max': 180, 'default': 90},
            'left_wrist': {'pin': 9, 'min': 0, 'max': 180, 'default': 90},
            'waist': {'pin': 10, 'min': 0, 'max': 180, 'default': 90},
            'base': {'pin': 11, 'min': 0, 'max': 180, 'default': 90},
        }
        
        # Current positions
        self.current_positions = {name: servo['default'] 
                                 for name, servo in self.servos.items()}
        
        # Initialize serial connection to Arduino
        try:
            port = config.get('hardware', {}).get('arduino_port', '/dev/ttyACM0')
            baud = config.get('hardware', {}).get('baud_rate', 9600)
            self.serial = serial.Serial(port, baud, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            logger.info(f"Connected to Arduino on {port}")
        except Exception as e:
            logger.error(f"Failed to connect to Arduino: {e}")
            self.serial = None
        
        # Reset to default positions
        self.reset_position()
    
    def move_servo(self, servo_name: str, angle: int, speed: float = 0.5):
        """
        Move servo to specified angle
        
        Args:
            servo_name: Name of servo
            angle: Target angle (0-180)
            speed: Movement speed (0.1-1.0)
        """
        if servo_name not in self.servos:
            logger.warning(f"Unknown servo: {servo_name}")
            return
        
        servo = self.servos[servo_name]
        
        # Clamp angle to limits
        angle = max(servo['min'], min(servo['max'], angle))
        
        # Smooth movement
        current = self.current_positions[servo_name]
        steps = abs(angle - current)
        delay = (1.0 - speed) * 0.02
        
        if steps > 0:
            step_size = 1 if angle > current else -1
            
            for pos in range(current, angle, step_size):
                self._set_servo_angle(servo['pin'], pos)
                time.sleep(delay)
            
            # Final position
            self._set_servo_angle(servo['pin'], angle)
            self.current_positions[servo_name] = angle
            
            logger.debug(f"Moved {servo_name} to {angle}°")
    
    def _set_servo_angle(self, pin: int, angle: int):
        """Send servo command to Arduino"""
        if self.serial and self.serial.is_open:
            try:
                command = f"S{pin:02d}A{angle:03d}\n"
                self.serial.write(command.encode())
            except Exception as e:
                logger.error(f"Error sending servo command: {e}")
    
    def reset_position(self):
        """Reset all servos to default positions"""
        logger.info("Resetting servos to default positions")
        
        for servo_name, servo in self.servos.items():
            self.move_servo(servo_name, servo['default'], speed=0.3)
    
    def get_position(self, servo_name: str) -> Optional[int]:
        """Get current servo position"""
        return self.current_positions.get(servo_name)
    
    def set_multiple(self, positions: Dict[str, int], speed: float = 0.5):
        """
        Set multiple servos simultaneously
        
        Args:
            positions: Dictionary of servo_name: angle
            speed: Movement speed
        """
        for servo_name, angle in positions.items():
            self.move_servo(servo_name, angle, speed)
    
    def disable_servo(self, servo_name: str):
        """Disable servo (remove power)"""
        if servo_name in self.servos:
            pin = self.servos[servo_name]['pin']
            if self.serial and self.serial.is_open:
                command = f"D{pin:02d}\n"
                self.serial.write(command.encode())
                logger.info(f"Disabled {servo_name}")
    
    def enable_servo(self, servo_name: str):
        """Enable servo"""
        if servo_name in self.servos:
            current_angle = self.current_positions[servo_name]
            self.move_servo(servo_name, current_angle)
            logger.info(f"Enabled {servo_name}")
    
    def cleanup(self):
        """Cleanup and close connections"""
        if self.serial and self.serial.is_open:
            self.reset_position()
            self.serial.close()
            logger.info("Servo controller cleanup complete")
