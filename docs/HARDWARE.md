# Hardware Assembly Guide

## 🔧 Assembly Overview

This guide will walk you through assembling your Hi-Tech Interactive Robot step by step.

## ⚠️ Safety First

- Disconnect all power before making connections
- Use proper ESD protection when handling electronics
- Double-check polarity before connecting power
- Keep workspace clean and organized
- Wear safety glasses when cutting or drilling

## 📋 Pre-Assembly Checklist

- [ ] All materials from MATERIALS.md acquired
- [ ] Tools ready and functional
- [ ] Workspace prepared with good lighting
- [ ] Component datasheets downloaded
- [ ] Wiring diagram printed or accessible

## 🏗️ Assembly Steps

### Step 1: Prepare the Chassis

1. **Unpack the robot frame/chassis**
2. **Identify mounting points** for:
   - Raspberry Pi
   - Arduino Mega
   - Servo motors
   - Power distribution board
   - Battery compartment

3. **Drill additional holes** if needed (use 3mm drill bit for M3 screws)

4. **Install standoffs** for mounting boards:
   - 4x standoffs for Raspberry Pi (M2.5 or M3)
   - 4x standoffs for Arduino Mega (M3)

### Step 2: Mount Main Controllers

1. **Mount Raspberry Pi 4**:
   - Secure with M2.5 or M3 screws
   - Ensure GPIO pins are accessible
   - Position for easy access to USB and HDMI ports

2. **Mount Arduino Mega**:
   - Secure with M3 screws
   - Position near servo connection area
   - Ensure USB port is accessible

3. **Mount Power Distribution Board**:
   - Central location for easy wiring
   - Secure firmly to prevent movement

### Step 3: Install Servo Motors

#### Head Assembly (2 servos)
1. **Head Pan Servo** (Pin 0):
   - Mount horizontally for left-right movement
   - Attach servo horn
   - Connect to Arduino pin 2

2. **Head Tilt Servo** (Pin 1):
   - Mount vertically for up-down movement
   - Stack on pan servo using bracket
   - Connect to Arduino pin 3

#### Right Arm (3 servos)
1. **Right Shoulder** (Pin 2) → Arduino pin 4
2. **Right Elbow** (Pin 3) → Arduino pin 5
3. **Right Wrist** (Pin 4) → Arduino pin 6

#### Left Arm (3 servos)
1. **Left Shoulder** (Pin 7) → Arduino pin 8
2. **Left Elbow** (Pin 8) → Arduino pin 9
3. **Left Wrist** (Pin 9) → Arduino pin 10

#### Body (2 servos)
1. **Waist** (Pin 10) → Arduino pin 11
2. **Base** (Pin 11) → Arduino pin 12

**Servo Mounting Tips**:
- Use U-brackets for secure mounting
- Ensure full range of motion (0-180°)
- Route cables neatly with cable ties
- Test each servo before final mounting

### Step 4: Wire Servo Connections

**Servo Wire Color Code**:
- **Brown/Black** = Ground (GND)
- **Red** = Power (VCC, 5-6V)
- **Orange/Yellow/White** = Signal (PWM)

**Wiring Scheme**:
```
Each Servo:
├── Signal Wire → Arduino Digital Pin
├── Power (Red) → 6V Power Rail
└── Ground (Brown) → Common Ground
```

**Important**:
- Connect all servo grounds together
- Connect all servo power to 6V rail (NOT 5V)
- Use separate power supply for servos
- Add 1000µF capacitor across power rails

### Step 5: Install Audio System

1. **USB Microphone**:
   - Connect to Raspberry Pi USB port
   - Position near robot's "face"
   - Secure with hot glue or bracket

2. **Speaker**:
   - Connect to Raspberry Pi 3.5mm jack OR
   - Connect via USB sound card
   - Mount in chassis with foam padding
   - Ensure sound can project outward

### Step 6: Install Camera

1. **Raspberry Pi Camera Module**:
   - Connect ribbon cable to Pi camera port
   - Mount on pan-tilt bracket
   - Position at "eye level"
   - Secure cable with clips

   **OR**

   **USB Webcam**:
   - Connect to Raspberry Pi USB port
   - Mount with adjustable bracket
   - Ensure clear field of view

### Step 7: Install LED Matrix

1. **Prepare LED Strip**:
   - Cut to 64 LEDs (8x8 matrix) if needed
   - Solder power wires to both ends
   - Add 470Ω resistor on data line

2. **Mount LED Matrix**:
   - Arrange in 8x8 grid pattern
   - Secure to diffuser panel
   - Mount on robot's "face" area

3. **Wire LED Strip**:
   ```
   LED Strip:
   ├── VCC (Red) → 5V Power Rail
   ├── GND (Black) → Common Ground
   └── Data (Green) → Raspberry Pi GPIO 18
   ```

4. **Add capacitor**: 1000µF across power lines near LED strip

### Step 8: Power System Setup

#### Power Distribution

```
Main Power Input (6V 5A)
├── Buck Converter #1 (6V → 5V 3A)
│   └── Raspberry Pi 4 (USB-C)
│
├── Buck Converter #2 (6V → 5V 2A)
│   └── LED Matrix
│
└── Direct 6V Rail
    └── All Servo Motors
```

**Wiring Steps**:

1. **Connect Main Power Supply**:
   - Input: 6V 5A DC adapter
   - Connect to power distribution board

2. **Setup Buck Converter #1** (for Raspberry Pi):
   - Input: 6V from main supply
   - Output: Adjust to 5.1V
   - Connect to USB-C cable for Pi

3. **Setup Buck Converter #2** (for LEDs):
   - Input: 6V from main supply
   - Output: Adjust to 5V
   - Connect to LED strip power

4. **Common Ground**:
   - Connect all grounds together:
     - Raspberry Pi ground
     - Arduino ground
     - Servo grounds
     - LED ground
     - Power supply ground

5. **Add Protection**:
   - 100µF capacitor on each buck converter output
   - 1000µF capacitor on servo power rail
   - Fuse on main power input (5A)

### Step 9: Connect Raspberry Pi to Arduino

**Serial Connection**:
```
Raspberry Pi          Arduino Mega
GPIO 14 (TXD) -----> RX1 (Pin 19)
GPIO 15 (RXD) <----- TX1 (Pin 18)
GND --------------- GND
```

**OR use USB connection**:
- Connect Arduino USB to Raspberry Pi USB port
- Simpler but uses USB port

### Step 10: Final Assembly

1. **Cable Management**:
   - Bundle wires with cable ties
   - Use velcro straps for removable sections
   - Label all connections
   - Ensure no wires interfere with moving parts

2. **Secure All Components**:
   - Double-check all screws
   - Ensure no loose wires
   - Test servo range of motion
   - Verify no short circuits

3. **Add Protective Covers** (optional):
   - Cover exposed electronics
   - Protect camera lens
   - Add decorative panels

## 🔌 Wiring Diagram

```
                    ┌─────────────────┐
                    │  6V 5A Power    │
                    │     Supply      │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   Power Dist.   │
                    │      Board      │
                    └─┬──────┬───────┬┘
                      │      │       │
            ┌─────────┘      │       └──────────┐
            │                │                  │
    ┌───────▼──────┐  ┌──────▼──────┐  ┌───────▼──────┐
    │ Buck Conv #1 │  │ Buck Conv #2│  │  6V Direct   │
    │   6V → 5V    │  │   6V → 5V   │  │   to Servos  │
    └───────┬──────┘  └──────┬──────┘  └───────┬──────┘
            │                │                  │
    ┌───────▼──────┐  ┌──────▼──────┐  ┌───────▼──────┐
    │ Raspberry Pi │  │  LED Matrix │  │ 12x Servos   │
    │      4       │  │   (8x8)     │  │              │
    └───────┬──────┘  └─────────────┘  └──────────────┘
            │
    ┌───────▼──────┐
    │ Arduino Mega │
    │ (via Serial) │
    └──────────────┘
```

## ✅ Post-Assembly Testing

### Power-On Sequence

1. **Visual Inspection**:
   - Check all connections
   - Verify no exposed wires
   - Ensure proper polarity

2. **Initial Power Test**:
   - Connect power supply (NO LOAD)
   - Measure voltages with multimeter:
     - Main rail: 6V
     - Buck #1 output: 5.0-5.1V
     - Buck #2 output: 5.0V
   - Disconnect power

3. **Component Testing**:
   - Connect Raspberry Pi only → Should boot
   - Connect Arduino only → LED should blink
   - Connect one servo → Should respond to test signal
   - Connect LED strip → Should light up

4. **Full System Test**:
   - Connect all components
   - Power on
   - Monitor current draw (should be <1A at idle)
   - Test each subsystem individually

## 🐛 Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Pi won't boot | Insufficient power | Check buck converter output, use 5.1V |
| Servos jittering | Power supply too weak | Use higher amperage supply, add capacitors |
| LEDs dim/flickering | Voltage drop | Shorten wires, add capacitor, separate power |
| No serial communication | Wrong pins/baud rate | Verify connections, check baud rate (9600) |
| Servo not moving | Wrong pin/connection | Check Arduino pin mapping, test servo separately |

## 📸 Assembly Photos

(Add photos of your build at each step)

## 🎓 Next Steps

After assembly:
1. Upload Arduino firmware (see arduino/servo_controller/)
2. Install software on Raspberry Pi (see docs/SOFTWARE.md)
3. Run initial tests (see docs/TESTING.md)
4. Calibrate servos (see docs/CALIBRATION.md)

---

**Assembly Time**: 4-6 hours
**Difficulty**: Intermediate
**Skills Required**: Basic soldering, electronics knowledge
