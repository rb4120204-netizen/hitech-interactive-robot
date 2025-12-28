/*
 * Arduino Servo Controller Firmware
 * Controls multiple servo motors via serial commands
 * 
 * Command Format: S[PIN]A[ANGLE]\n
 * Example: S00A090\n (Set servo on pin 0 to 90 degrees)
 * 
 * Disable Command: D[PIN]\n
 * Example: D00\n (Disable servo on pin 0)
 */

#include <Servo.h>

#define MAX_SERVOS 12
#define BAUD_RATE 9600

Servo servos[MAX_SERVOS];
int servoPins[MAX_SERVOS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
bool servoAttached[MAX_SERVOS] = {false};

String inputString = "";
boolean stringComplete = false;

void setup() {
  Serial.begin(BAUD_RATE);
  inputString.reserve(20);
  
  // Initialize all servos
  for (int i = 0; i < MAX_SERVOS; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90);  // Center position
    servoAttached[i] = true;
    delay(100);
  }
  
  Serial.println("Arduino Servo Controller Ready");
}

void loop() {
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

void processCommand(String command) {
  command.trim();
  
  if (command.length() < 3) {
    Serial.println("ERROR: Invalid command length");
    return;
  }
  
  char cmdType = command.charAt(0);
  
  if (cmdType == 'S') {
    // Servo move command: S[PIN]A[ANGLE]
    int pinIndex = command.substring(1, 3).toInt();
    int angleIndex = command.indexOf('A');
    
    if (angleIndex == -1 || pinIndex >= MAX_SERVOS) {
      Serial.println("ERROR: Invalid servo command");
      return;
    }
    
    int angle = command.substring(angleIndex + 1).toInt();
    
    // Validate angle
    if (angle < 0 || angle > 180) {
      Serial.println("ERROR: Angle out of range (0-180)");
      return;
    }
    
    // Attach servo if not attached
    if (!servoAttached[pinIndex]) {
      servos[pinIndex].attach(servoPins[pinIndex]);
      servoAttached[pinIndex] = true;
    }
    
    // Move servo
    servos[pinIndex].write(angle);
    
    Serial.print("OK: Servo ");
    Serial.print(pinIndex);
    Serial.print(" -> ");
    Serial.println(angle);
  }
  else if (cmdType == 'D') {
    // Disable servo command: D[PIN]
    int pinIndex = command.substring(1, 3).toInt();
    
    if (pinIndex >= MAX_SERVOS) {
      Serial.println("ERROR: Invalid pin index");
      return;
    }
    
    if (servoAttached[pinIndex]) {
      servos[pinIndex].detach();
      servoAttached[pinIndex] = false;
      Serial.print("OK: Servo ");
      Serial.print(pinIndex);
      Serial.println(" disabled");
    }
  }
  else if (cmdType == 'R') {
    // Reset all servos to center
    for (int i = 0; i < MAX_SERVOS; i++) {
      if (!servoAttached[i]) {
        servos[i].attach(servoPins[i]);
        servoAttached[i] = true;
      }
      servos[i].write(90);
      delay(50);
    }
    Serial.println("OK: All servos reset");
  }
  else {
    Serial.println("ERROR: Unknown command");
  }
}
