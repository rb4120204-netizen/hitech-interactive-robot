"""
LED Controller Module
Controls LED matrix for robot expressions
"""

import time
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class LEDController:
    """LED matrix controller for robot expressions"""
    
    def __init__(self, config):
        """Initialize LED controller"""
        self.config = config
        
        # LED configuration
        self.num_leds = config.get('hardware', {}).get('num_leds', 64)
        self.brightness = config.get('hardware', {}).get('led_brightness', 0.5)
        
        # Try to initialize LED hardware
        try:
            # For WS2812B LED strip
            import board
            import neopixel
            
            self.pixels = neopixel.NeoPixel(
                board.D18,
                self.num_leds,
                brightness=self.brightness,
                auto_write=False
            )
            self.hardware_available = True
            logger.info("LED hardware initialized")
        except Exception as e:
            logger.warning(f"LED hardware not available: {e}")
            self.hardware_available = False
            self.pixels = None
        
        # Expression patterns (8x8 matrix)
        self.expressions = self._load_expressions()
        
        # Current expression
        self.current_expression = "neutral"
    
    def _load_expressions(self) -> Dict:
        """Load LED expression patterns"""
        return {
            'happy': [
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 1, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
            ],
            'sad': [
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
            ],
            'neutral': [
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
            ],
            'surprised': [
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
            ],
            'angry': [
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
            ],
            'listening': [
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
            ],
            'sleep': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
        }
    
    def set_expression(self, expression: str, color: Tuple[int, int, int] = (0, 255, 0)):
        """
        Set LED expression
        
        Args:
            expression: Expression name
            color: RGB color tuple
        """
        if expression not in self.expressions:
            logger.warning(f"Unknown expression: {expression}")
            return
        
        logger.info(f"Setting expression: {expression}")
        self.current_expression = expression
        
        if not self.hardware_available:
            return
        
        pattern = self.expressions[expression]
        
        # Convert 8x8 pattern to LED strip
        for row in range(8):
            for col in range(8):
                led_index = row * 8 + col
                if led_index < self.num_leds:
                    if pattern[row][col] == 1:
                        self.pixels[led_index] = color
                    else:
                        self.pixels[led_index] = (0, 0, 0)
        
        self.pixels.show()
    
    def set_color(self, color: Tuple[int, int, int]):
        """Set all LEDs to single color"""
        if not self.hardware_available:
            return
        
        self.pixels.fill(color)
        self.pixels.show()
    
    def turn_off(self):
        """Turn off all LEDs"""
        logger.info("Turning off LEDs")
        if self.hardware_available:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
    
    def blink(self, times: int = 3, color: Tuple[int, int, int] = (0, 255, 0)):
        """Blink LEDs"""
        for _ in range(times):
            self.set_color(color)
            time.sleep(0.3)
            self.turn_off()
            time.sleep(0.3)
    
    def pulse(self, color: Tuple[int, int, int] = (0, 255, 0), duration: float = 2.0):
        """Pulse effect"""
        if not self.hardware_available:
            return
        
        steps = 50
        for i in range(steps):
            brightness = (i / steps) if i < steps // 2 else ((steps - i) / steps)
            adjusted_color = tuple(int(c * brightness) for c in color)
            self.set_color(adjusted_color)
            time.sleep(duration / steps)
    
    def rainbow_cycle(self, duration: float = 3.0):
        """Rainbow cycle effect"""
        if not self.hardware_available:
            return
        
        def wheel(pos):
            if pos < 85:
                return (pos * 3, 255 - pos * 3, 0)
            elif pos < 170:
                pos -= 85
                return (255 - pos * 3, 0, pos * 3)
            else:
                pos -= 170
                return (0, pos * 3, 255 - pos * 3)
        
        steps = 256
        for j in range(steps):
            for i in range(self.num_leds):
                pixel_index = (i * 256 // self.num_leds) + j
                self.pixels[i] = wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(duration / steps)
    
    def set_brightness(self, brightness: float):
        """
        Set LED brightness
        
        Args:
            brightness: Brightness level (0.0-1.0)
        """
        self.brightness = max(0.0, min(1.0, brightness))
        if self.hardware_available:
            self.pixels.brightness = self.brightness
            self.pixels.show()
        logger.info(f"Brightness set to {self.brightness}")
