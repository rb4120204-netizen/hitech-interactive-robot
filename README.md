# Hi-Tech Interactive Robot 🤖

A sophisticated interactive robot system with voice recognition, speech synthesis, and gesture control capabilities.

## Features

- 🎤 **Voice Recognition**: Understands and responds to voice commands
- 🔊 **Text-to-Speech**: Natural voice responses
- 👋 **Gesture Control**: Performs various physical gestures
- 🤖 **Servo Control**: Smooth movement control for arms, head, and body
- 👁️ **Computer Vision**: Face detection and object recognition
- 💡 **LED Expressions**: Visual feedback through LED matrix
- 🧠 **AI Integration**: Natural language processing

## System Architecture

```
┌─────────────────────────────────────────┐
│         Hi-Tech Robot System            │
├─────────────────────────────────────────┤
│  Hardware Layer                         │
│  - Raspberry Pi 4 (Main Controller)     │
│  - Arduino Mega (Servo Controller)      │
│  - Microphone Array                     │
│  - Speaker System                       │
│  - Camera Module                        │
│  - Servo Motors (x12)                   │
│  - LED Matrix Display                   │
├─────────────────────────────────────────┤
│  Software Layer                         │
│  - Speech Recognition (Google/Vosk)     │
│  - TTS Engine (pyttsx3/gTTS)           │
│  - Gesture Controller                   │
│  - Vision Processing (OpenCV)           │
│  - AI Brain (NLP)                       │
└─────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/rb4120204-netizen/hitech-interactive-robot.git
cd hitech-interactive-robot

# Install dependencies
pip install -r requirements.txt

# Run the robot
python main.py
```

## Hardware Requirements

See [MATERIALS.md](MATERIALS.md) for complete list

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Hardware Assembly](docs/HARDWARE.md)
- [Software Configuration](docs/SOFTWARE.md)
- [API Reference](docs/API.md)

## Project Structure

```
hitech-interactive-robot/
├── main.py                 # Main entry point
├── config/
│   └── settings.yaml       # Configuration
├── src/
│   ├── speech/            # Speech recognition & TTS
│   ├── gesture/           # Gesture control
│   ├── vision/            # Computer vision
│   ├── hardware/          # Hardware interfaces
│   └── ai/                # AI processing
├── arduino/               # Arduino firmware
├── docs/                  # Documentation
└── tests/                 # Unit tests
```

## License

MIT License - See LICENSE file

## Author

Rakesh Behera
