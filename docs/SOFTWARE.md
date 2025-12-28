# Software Setup Guide

## 🖥️ Raspberry Pi Setup

### Step 1: Install Raspberry Pi OS

1. **Download Raspberry Pi Imager**: https://www.raspberrypi.com/software/
2. **Flash OS to SD Card**:
   - Choose "Raspberry Pi OS (64-bit)" with desktop
   - Select your SD card
   - Configure settings (hostname, WiFi, SSH)
   - Write to card

3. **First Boot**:
   - Insert SD card into Raspberry Pi
   - Connect monitor, keyboard, mouse
   - Power on and complete setup wizard

### Step 2: System Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Enable required interfaces
sudo raspi-config
# Navigate to: Interface Options
# Enable: Camera, Serial Port, I2C, SPI

# Install system dependencies
sudo apt install -y python3-pip python3-dev git
sudo apt install -y portaudio19-dev python3-pyaudio
sudo apt install -y espeak libespeak-dev
sudo apt install -y libatlas-base-dev libopenblas-dev
sudo apt install -y python3-opencv
```

### Step 3: Clone Repository

```bash
cd ~
git clone https://github.com/rb4120204-netizen/hitech-interactive-robot.git
cd hitech-interactive-robot
```

### Step 4: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install additional system packages
sudo apt install -y python3-rpi.gpio
```

### Step 5: Configure Audio

```bash
# Test microphone
arecord -l  # List recording devices
arecord -d 5 test.wav  # Record 5 second test

# Test speaker
aplay -l  # List playback devices
speaker-test -t wav -c 2  # Test speakers

# Set default audio device (if needed)
sudo nano /etc/asound.conf
# Add:
# pcm.!default {
#     type hw
#     card 1
# }
# ctl.!default {
#     type hw
#     card 1
# }
```

### Step 6: Configure Camera

```bash
# Test camera
raspistill -o test.jpg  # Take test photo
raspivid -o test.h264 -t 5000  # Record 5 second video

# For USB webcam
v4l2-ctl --list-devices  # List video devices
```

## 🔧 Arduino Setup

### Step 1: Install Arduino IDE

**On your computer** (not Raspberry Pi):
1. Download Arduino IDE: https://www.arduino.cc/en/software
2. Install and launch

### Step 2: Upload Firmware

1. **Open firmware**:
   - File → Open → Navigate to `arduino/servo_controller/servo_controller.ino`

2. **Select board**:
   - Tools → Board → Arduino AVR Boards → Arduino Mega 2560

3. **Select port**:
   - Tools → Port → (Select your Arduino's port)

4. **Upload**:
   - Click Upload button (→)
   - Wait for "Done uploading"

5. **Test**:
   - Open Serial Monitor (Ctrl+Shift+M)
   - Set baud rate to 9600
   - Should see "Arduino Servo Controller Ready"

### Step 3: Connect to Raspberry Pi

```bash
# Find Arduino port
ls /dev/ttyACM* /dev/ttyUSB*

# Test connection
sudo apt install -y screen
screen /dev/ttyACM0 9600
# Type: R (should reset all servos)
# Ctrl+A then K to exit

# Give user permission
sudo usermod -a -G dialout $USER
# Logout and login for changes to take effect
```

## ⚙️ Configuration

### Edit Configuration File

```bash
cd ~/hitech-interactive-robot
nano config/settings.yaml
```

**Key settings to verify**:
```yaml
hardware:
  arduino_port: "/dev/ttyACM0"  # Update if different
  
vision:
  camera_index: 0  # 0 for first camera
  
speech:
  language: "en-US"  # Change for your language
```

## 🧪 Testing

### Test Individual Components

```bash
cd ~/hitech-interactive-robot
source venv/bin/activate

# Test speech recognition
python3 -c "
from src.speech.speech_recognizer import SpeechRecognizer
from config.config_loader import load_config
sr = SpeechRecognizer(load_config())
print('Say something...')
text = sr.listen()
print(f'You said: {text}')
"

# Test text-to-speech
python3 -c "
from src.speech.text_to_speech import TextToSpeech
from config.config_loader import load_config
tts = TextToSpeech(load_config())
tts.speak('Hello, I am your robot!')
"

# Test servo control
python3 -c "
from src.hardware.servo_controller import ServoController
from config.config_loader import load_config
servo = ServoController(load_config())
servo.move_servo('head_pan', 90)
import time
time.sleep(1)
servo.reset_position()
"

# Test camera
python3 -c "
from src.vision.vision_processor import VisionProcessor
from config.config_loader import load_config
vision = VisionProcessor(load_config())
img = vision.capture_image('test_capture.jpg')
print('Image captured!')
vision.cleanup()
"
```

## 🚀 Running the Robot

### Manual Start

```bash
cd ~/hitech-interactive-robot
source venv/bin/activate
python3 main.py
```

### Auto-Start on Boot (Optional)

```bash
# Create systemd service
sudo nano /etc/systemd/system/robot.service
```

Add:
```ini
[Unit]
Description=Interactive Robot Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/hitech-interactive-robot
ExecStart=/home/pi/hitech-interactive-robot/venv/bin/python3 /home/pi/hitech-interactive-robot/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable robot.service
sudo systemctl start robot.service

# Check status
sudo systemctl status robot.service

# View logs
sudo journalctl -u robot.service -f
```

## 🐛 Troubleshooting

### Common Issues

**1. "Permission denied" on serial port**
```bash
sudo usermod -a -G dialout $USER
# Logout and login
```

**2. "No module named 'RPi'"**
```bash
pip install RPi.GPIO
```

**3. Microphone not working**
```bash
# Check if detected
arecord -l

# Test recording
arecord -D plughw:1,0 -d 5 test.wav
aplay test.wav
```

**4. Camera not detected**
```bash
# Enable camera
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot
sudo reboot
```

**5. Servos not responding**
```bash
# Check Arduino connection
ls /dev/ttyACM*

# Test Arduino directly
screen /dev/ttyACM0 9600
# Type: S00A090 (move servo 0 to 90°)
```

**6. Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📊 Performance Optimization

### Reduce CPU Usage

```bash
# Disable desktop (if not needed)
sudo systemctl set-default multi-user.target

# Limit camera resolution in config/settings.yaml
vision:
  resolution: [320, 240]  # Lower resolution
```

### Improve Response Time

```bash
# Overclock (optional, increases heat)
sudo nano /boot/config.txt
# Add:
# over_voltage=2
# arm_freq=1750
```

## 🔄 Updates

```bash
cd ~/hitech-interactive-robot
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📝 Next Steps

1. Calibrate servos (see docs/CALIBRATION.md)
2. Train custom voice commands
3. Add custom gestures
4. Customize LED expressions

---

**Setup Time**: 1-2 hours
**Difficulty**: Intermediate
