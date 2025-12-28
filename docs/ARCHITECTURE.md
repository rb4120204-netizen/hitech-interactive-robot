# System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                    │
│  Voice Input → Microphone → Speech Recognition → AI Brain   │
│  AI Brain → Text-to-Speech → Speaker → Voice Output         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER (Python)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Speech     │  │   Gesture    │  │   Vision     │     │
│  │  Recognizer  │  │  Controller  │  │  Processor   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     TTS      │  │   AI Brain   │  │     LED      │     │
│  │    Engine    │  │     (NLP)    │  │  Controller  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    HARDWARE ABSTRACTION LAYER                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Servo     │  │     LED      │  │    Camera    │     │
│  │  Controller  │  │  Controller  │  │   Interface  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      HARDWARE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Raspberry Pi │  │   Arduino    │  │   Sensors    │     │
│  │      4       │  │     Mega     │  │  & Actuators │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                  ↓                  ↓             │
│  ┌──────────────────────────────────────────────────┐      │
│  │  12x Servos | LED Matrix | Camera | Mic | Speaker│      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Voice Command Processing

```
1. User speaks → Microphone captures audio
2. Speech Recognizer converts to text
3. AI Brain processes command
4. Determines action + response
5. Gesture Controller executes movement
6. TTS Engine generates speech
7. Speaker outputs response
8. LED Controller shows expression
```

### Vision Processing

```
1. Camera captures frame
2. Vision Processor analyzes image
3. Detects faces/objects/motion
4. Sends data to AI Brain
5. AI Brain decides action
6. Servo Controller adjusts head position
7. LED shows visual feedback
```

## 🧩 Component Interaction

### Main Controller (Raspberry Pi 4)
**Responsibilities:**
- Run Python application
- Speech recognition
- Text-to-speech
- Computer vision
- AI processing
- Coordinate all subsystems

**Interfaces:**
- USB: Microphone, Speaker, Camera, Arduino
- GPIO: LED strip control
- Network: Updates, cloud services

### Servo Controller (Arduino Mega)
**Responsibilities:**
- Control 12 servo motors
- Smooth movement interpolation
- Position feedback
- Safety limits

**Communication:**
- Serial UART (9600 baud)
- Command format: `S[PIN]A[ANGLE]`
- Response: Status messages

### Speech System
**Input Path:**
```
Microphone → USB Audio → PyAudio → 
SpeechRecognition → Google API → Text
```

**Output Path:**
```
Text → pyttsx3 Engine → Audio Buffer → 
USB Audio → Speaker
```

### Vision System
```
Camera → USB/CSI → OpenCV → 
Image Processing → Feature Detection → 
AI Brain
```

## 📊 Module Dependencies

```
main.py
├── config_loader.py
├── speech_recognizer.py
│   └── SpeechRecognition library
├── text_to_speech.py
│   └── pyttsx3 library
├── gesture_controller.py
│   └── servo_controller.py
│       └── pyserial library
├── vision_processor.py
│   └── OpenCV library
├── led_controller.py
│   └── neopixel library
└── brain.py
    └── NLTK/regex
```

## 🔌 Communication Protocols

### Serial Communication (Pi ↔ Arduino)
- **Protocol:** UART
- **Baud Rate:** 9600
- **Data Bits:** 8
- **Parity:** None
- **Stop Bits:** 1

**Command Structure:**
```
Servo Move:  S[PIN:2]A[ANGLE:3]\n
Disable:     D[PIN:2]\n
Reset:       R\n
```

### GPIO Communication (Pi ↔ LED)
- **Protocol:** WS2812B (NeoPixel)
- **Pin:** GPIO 18 (PWM)
- **Voltage:** 5V logic
- **Data Rate:** 800kHz

### USB Communication
- **Microphone:** USB Audio Class
- **Speaker:** USB Audio Class
- **Camera:** USB Video Class / CSI
- **Arduino:** USB CDC (Serial)

## 🧠 AI Brain Logic

```python
Command Input
    ↓
Pattern Matching (Regex)
    ↓
Intent Recognition
    ↓
Context Analysis
    ↓
Action Selection
    ↓
Response Generation
    ↓
Multi-modal Output:
├── Speech (TTS)
├── Gesture (Servos)
└── Expression (LEDs)
```

## ⚡ Power Distribution

```
6V 5A Main Supply
├── Buck Converter #1 (5V 3A)
│   └── Raspberry Pi 4
├── Buck Converter #2 (5V 2A)
│   └── LED Matrix
└── Direct 6V
    └── 12x Servo Motors
        (Peak: 500mA each)
```

## 🔒 Safety Features

1. **Servo Limits:** Software angle constraints (0-180°)
2. **Power Protection:** Capacitors on all power rails
3. **Thermal Management:** Heat sinks on regulators
4. **Error Handling:** Try-catch blocks in all modules
5. **Graceful Shutdown:** Cleanup on exit

## 📈 Performance Characteristics

| Metric | Value |
|--------|-------|
| Voice Recognition Latency | 1-2 seconds |
| Speech Response Time | 0.5-1 second |
| Servo Movement Speed | 60°/second |
| Camera Frame Rate | 30 FPS |
| LED Update Rate | 60 Hz |
| Command Processing | <100ms |

## 🔄 State Machine

```
┌─────────┐
│  IDLE   │ ←──────────────────┐
└────┬────┘                    │
     │ Voice detected          │
     ↓                         │
┌─────────┐                    │
│LISTENING│                    │
└────┬────┘                    │
     │ Command received        │
     ↓                         │
┌─────────┐                    │
│PROCESSING│                   │
└────┬────┘                    │
     │ Action determined       │
     ↓                         │
┌─────────┐                    │
│EXECUTING│                    │
└────┬────┘                    │
     │ Action complete         │
     ↓                         │
┌─────────┐                    │
│RESPONDING│                   │
└────┬────┘                    │
     │ Response delivered      │
     └─────────────────────────┘
```

## 🛠️ Extensibility Points

### Add New Gestures
```python
# In gesture_controller.py
def custom_gesture(self):
    moves = [
        {'servo': 'right_shoulder', 'angle': 90},
        {'servo': 'right_elbow', 'angle': 45},
    ]
    self._execute_gesture_sequence(moves)
```

### Add New Commands
```python
# In brain.py
self.command_patterns['custom'] = {
    'patterns': [r'custom command'],
    'action': 'custom_gesture',
    'speech': 'Executing custom action!',
}
```

### Add New Vision Features
```python
# In vision_processor.py
def detect_custom_object(self):
    # Your detection logic
    pass
```

---

**Architecture Version:** 1.0
**Last Updated:** December 2025
