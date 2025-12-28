"""
Configuration Loader
Loads and manages robot configuration
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config/settings.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return get_default_config()
    else:
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        'robot': {
            'name': 'Interactive Robot',
            'version': '1.0.0',
        },
        'speech': {
            'language': 'en-US',
            'timeout': 5,
            'phrase_time_limit': 10,
        },
        'tts': {
            'voice_id': 0,
            'rate': 150,
            'volume': 1.0,
        },
        'hardware': {
            'arduino_port': '/dev/ttyACM0',
            'baud_rate': 9600,
            'num_leds': 64,
            'led_brightness': 0.5,
        },
        'vision': {
            'camera_index': 0,
            'resolution': [640, 480],
        },
        'logging': {
            'level': 'INFO',
            'file': 'robot.log',
        },
    }


def save_config(config: Dict[str, Any], config_path: str = 'config/settings.yaml'):
    """
    Save configuration to YAML file
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        logger.info(f"Configuration saved to {config_path}")
    except Exception as e:
        logger.error(f"Error saving config: {e}")
