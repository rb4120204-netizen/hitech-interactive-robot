# Hi-Tech Interactive Robot - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- ✅ Hardware assembled (see [HARDWARE.md](docs/HARDWARE.md))
- ✅ Raspberry Pi with OS installed
- ✅ Arduino firmware uploaded

### Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/rb4120204-netizen/hitech-interactive-robot.git
cd hitech-interactive-robot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure (edit if needed)
nano config/settings.yaml

# 4. Run the robot!
python3 main.py
```

## 🎤 Voice Commands

Once running, try these commands:

| Say This | Robot Does |
|----------|-----------|
| "Hello" / "Hi" | Greets you back |
| "Wave" | Waves hand |
| "Nod" | Nods head yes |
| "Shake head" | Shakes head no |
| "Dance" | Performs dance moves |
| "Thumbs up" | Shows thumbs up |
| "Point left/right" | Points in direction |
| "Take a photo" | Captures image |
| "Look around" | Scans environment |
| "What can you do?" | Lists capabilities |

## 🎨 LED Expressions

The robot shows emotions through LED matrix:
- 😊 **Happy** - Smiling face
- 😢 **Sad** - Frowning face
- 😐 **Neutral** - Straight face
- 😮 **Surprised** - Wide eyes
- 😠 **Angry** - Angry eyebrows
- 👂 **Listening** - Pulsing animation
- 😴 **Sleep** - Closed eyes

## 🤖 Robot Capabilities

### Voice Interaction
- Listens to your commands
- Responds with natural speech
- Understands context

### Physical Gestures
- Wave hello
- Nod yes/no
- Point directions
- Thumbs up
- Dance moves
- Look around

### Vision
- Face detection
- Object tracking
- Motion detection
- Photo capture

### Expressions
- LED facial expressions
- Color animations
- Status indicators

## 📁 Project Structure

```
hitech-interactive-robot/
├── main.py                    # Start here!
├── requirements.txt           # Python dependencies
├── config/
│   ├── settings.yaml         # Configuration
│   └── config_loader.py      # Config handler
├── src/
│   ├── speech/               # Voice recognition & TTS
│   │   ├── speech_recognizer.py
│   │   └── text_to_speech.py
│   ├── gesture/              # Movement control
│   │   └── gesture_controller.py
│   ├── vision/               # Computer vision
│   │   └── vision_processor.py
│   ├── hardware/             # Hardware interfaces
│   │   ├── servo_controller.py
│   │   └── led_controller.py
│   └── ai/                   # AI brain
│       └── brain.py
├── arduino/                  # Arduino firmware
│   └── servo_controller/
│       └── servo_controller.ino
└── docs/                     # Documentation
    ├── HARDWARE.md          # Assembly guide
    └── SOFTWARE.md          # Setup guide
```

## 🔧 Configuration

Edit `config/settings.yaml` to customize:

```yaml
# Change language
speech:
  language: "en-US"  # Try: es-ES, fr-FR, de-DE

# Adjust voice
tts:
  rate: 150      # Speed (50-300)
  volume: 1.0    # Volume (0.0-1.0)

# Arduino port
hardware:
  arduino_port: "/dev/ttyACM0"  # Update if different
```

## 🐛 Common Issues

**Robot not responding to voice?**
```bash
# Test microphone
arecord -d 5 test.wav && aplay test.wav
```

**Servos not moving?**
```bash
# Check Arduino connection
ls /dev/ttyACM*
```

**Camera not working?**
```bash
# Enable camera
sudo raspi-config
# Interface Options → Camera → Enable
```

## 📚 Full Documentation

- 📦 [Materials List](MATERIALS.md) - What to buy
- 🔧 [Hardware Assembly](docs/HARDWARE.md) - Build guide
- 💻 [Software Setup](docs/SOFTWARE.md) - Installation
- 🎯 [API Reference](docs/API.md) - Programming guide

## 🆘 Need Help?

1. Check [Troubleshooting](docs/SOFTWARE.md#troubleshooting)
2. Review [Hardware Guide](docs/HARDWARE.md)
3. Open an issue on GitHub

## 🎓 Next Steps

1. ✅ Get basic system running
2. 🎯 Calibrate servos for smooth movement
3. 🎨 Customize LED expressions
4. 🗣️ Add custom voice commands
5. 🤖 Create new gestures
6. 📸 Implement object recognition

## 💡 Tips

- Start with simple commands
- Speak clearly and wait for response
- Keep robot in well-lit area for vision
- Ensure stable power supply
- Monitor logs for debugging

## 🌟 Features to Explore

- **Voice Training**: Teach custom commands
- **Gesture Programming**: Create complex movements
- **Vision Tasks**: Face tracking, object detection
- **LED Animations**: Custom light patterns
- **Remote Control**: Add web interface
- **AI Integration**: Connect to ChatGPT/Claude

---

**Ready to build?** Start with [MATERIALS.md](MATERIALS.md)!

**Need help?** Check [docs/](docs/) folder!

**Have fun building! 🤖✨**
