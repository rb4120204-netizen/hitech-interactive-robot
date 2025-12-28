"""
Robot Brain - AI Processing Module
Handles natural language understanding and decision making
"""

import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RobotBrain:
    """AI brain for processing commands and making decisions"""
    
    def __init__(self, config):
        """Initialize robot brain"""
        self.config = config
        
        # Command patterns
        self.command_patterns = self._load_command_patterns()
        
        # Context memory
        self.context = {
            'last_command': None,
            'conversation_history': [],
            'user_preferences': {},
        }
        
        logger.info("Robot brain initialized")
    
    def _load_command_patterns(self) -> Dict:
        """Load command recognition patterns"""
        return {
            'greet': {
                'patterns': [r'hello', r'hi', r'hey', r'greetings'],
                'action': 'greet',
                'speech': 'Hello! How can I help you?',
                'expression': 'happy',
            },
            'wave': {
                'patterns': [r'wave', r'say hi', r'greet'],
                'action': 'wave',
                'speech': 'Waving hello!',
                'expression': 'happy',
            },
            'nod': {
                'patterns': [r'nod', r'yes', r'agree', r'confirm'],
                'action': 'nod',
                'speech': 'Yes, I understand.',
                'expression': 'neutral',
            },
            'shake_head': {
                'patterns': [r'shake.*head', r'no', r'disagree', r'deny'],
                'action': 'shake_head',
                'speech': 'No, I don\'t think so.',
                'expression': 'neutral',
            },
            'dance': {
                'patterns': [r'dance', r'move', r'groove'],
                'action': 'dance',
                'speech': 'Let me dance for you!',
                'expression': 'happy',
            },
            'look_around': {
                'patterns': [r'look around', r'scan', r'observe'],
                'action': 'look_around',
                'speech': 'Looking around...',
                'expression': 'neutral',
            },
            'take_photo': {
                'patterns': [r'take.*photo', r'picture', r'capture', r'snap'],
                'action': 'take_photo',
                'speech': 'Taking a photo!',
                'expression': 'neutral',
            },
            'detect_face': {
                'patterns': [r'detect.*face', r'find.*face', r'see.*face'],
                'action': 'detect_face',
                'speech': 'Scanning for faces...',
                'expression': 'neutral',
            },
            'point_left': {
                'patterns': [r'point.*left'],
                'action': 'point',
                'parameters': {'direction': 'left'},
                'speech': 'Pointing left.',
                'expression': 'neutral',
            },
            'point_right': {
                'patterns': [r'point.*right'],
                'action': 'point',
                'parameters': {'direction': 'right'},
                'speech': 'Pointing right.',
                'expression': 'neutral',
            },
            'thumbs_up': {
                'patterns': [r'thumbs up', r'good job', r'well done', r'approve'],
                'action': 'thumbs_up',
                'speech': 'Thumbs up!',
                'expression': 'happy',
            },
            'introduce': {
                'patterns': [r'who are you', r'introduce', r'what.*your name'],
                'action': None,
                'speech': 'I am an interactive robot. I can listen to your commands, speak, and perform gestures. How can I assist you?',
                'expression': 'happy',
            },
            'capabilities': {
                'patterns': [r'what can you do', r'capabilities', r'features', r'help'],
                'action': None,
                'speech': 'I can wave, nod, shake my head, dance, point, take photos, detect faces, and respond to your voice commands. Just tell me what you need!',
                'expression': 'happy',
            },
            'goodbye': {
                'patterns': [r'goodbye', r'bye', r'see you', r'farewell'],
                'action': None,
                'speech': 'Goodbye! It was nice talking to you!',
                'expression': 'happy',
            },
        }
    
    def process(self, command: str) -> Dict[str, Any]:
        """
        Process voice command and generate response
        
        Args:
            command: Voice command text
            
        Returns:
            Dictionary with action, speech, expression, parameters
        """
        logger.info(f"Processing command: {command}")
        
        # Store in context
        self.context['last_command'] = command
        self.context['conversation_history'].append(command)
        
        # Keep only last 10 commands
        if len(self.context['conversation_history']) > 10:
            self.context['conversation_history'].pop(0)
        
        # Match command pattern
        for cmd_name, cmd_data in self.command_patterns.items():
            for pattern in cmd_data['patterns']:
                if re.search(pattern, command, re.IGNORECASE):
                    logger.info(f"Matched command: {cmd_name}")
                    return {
                        'action': cmd_data.get('action'),
                        'speech': cmd_data.get('speech'),
                        'expression': cmd_data.get('expression', 'neutral'),
                        'parameters': cmd_data.get('parameters', {}),
                    }
        
        # No match found
        logger.info("No command match found")
        return {
            'action': None,
            'speech': 'I didn\'t understand that. Can you please repeat?',
            'expression': 'neutral',
            'parameters': {},
        }
    
    def add_custom_command(self, name: str, patterns: list, action: str, 
                          speech: str, expression: str = 'neutral'):
        """
        Add custom command pattern
        
        Args:
            name: Command name
            patterns: List of regex patterns
            action: Action to execute
            speech: Response speech
            expression: LED expression
        """
        self.command_patterns[name] = {
            'patterns': patterns,
            'action': action,
            'speech': speech,
            'expression': expression,
        }
        logger.info(f"Added custom command: {name}")
    
    def get_context(self) -> Dict:
        """Get current context"""
        return self.context.copy()
    
    def clear_context(self):
        """Clear conversation context"""
        self.context['conversation_history'] = []
        logger.info("Context cleared")
