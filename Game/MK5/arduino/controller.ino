#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <Wire.h>
#include <BleGamepad.h>

MPU6050 mpu;
BleGamepad bleGamepad("ESP32 DMP Gamepad", "OpenAI", 100);

// DMP Variablen
bool dmpReady = false;
uint8_t mpuIntStatus;
uint8_t devStatus;
uint16_t packetSize;
uint16_t fifoCount;
uint8_t fifoBuffer[64];

#define CALIB_BUTTON_PIN 2

// Orientierung
Quaternion q;
VectorFloat gravity;
float ypr[3];  // yaw, pitch, roll

// Kalibrierung
bool calibrated = false;
float pitchOffset = 0;
float rollOffset = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(CALIB_BUTTON_PIN, INPUT);

  mpu.initialize();
  devStatus = mpu.dmpInitialize();

  if (devStatus == 0) {
    // Setze DMP-Output-Rate auf 50 Hz
    mpu.setDMPEnabled(true);
    dmpReady = true;
    packetSize = mpu.dmpGetFIFOPacketSize();
    Serial.println("DMP ready!");
  } else {
    Serial.print("DMP init failed (code ");
    Serial.print(devStatus);
    Serial.println(")");
    while (1)
      ;
  }

  bleGamepad.begin();
}

void loop() {
  if (!dmpReady || !bleGamepad.isConnected()) return;

  fifoCount = mpu.getFIFOCount();
  if (fifoCount < packetSize) return;

  if (fifoCount >= 1024) {
    mpu.resetFIFO();  // FIFO Overflow
    Serial.println("FIFO overflow!");
    return;
  }

  while (fifoCount >= packetSize) {
    mpu.getFIFOBytes(fifoBuffer, packetSize);
    fifoCount -= packetSize;
  }

  // Orientierung berechnen
  mpu.dmpGetQuaternion(&q, fifoBuffer);
  mpu.dmpGetGravity(&gravity, &q);
  mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

  // Umrechnung auf Grad
  float yaw = ypr[0] * 180 / M_PI;
  float pitch = ypr[1] * 180 / M_PI;
  float roll = ypr[2] * 180 / M_PI;

  // === Kalibrierung per Button ===
if (digitalRead(CALIB_BUTTON_PIN) == HIGH) {
    pitchOffset = pitch;
    rollOffset = roll;
    calibrated = true;
    mpu.resetFIFO();  // <<< wichtig!
    Serial.print("Manuell neu kalibriert (richtige Werte gespeichert). ");
    Serial.print("Pitch Offset: "); Serial.print(pitchOffset);
    Serial.print(" | Roll Offset: "); Serial.println(rollOffset);
    delay(500);
}

  // Automatische Kalibrierung beim ersten Mal
  if (!calibrated && millis() > 1000) {
    pitchOffset = pitch;
    rollOffset = roll;
    calibrated = true;
    Serial.println("Kalibriert.");
  }

  // Offset-Korrektur
  float pitchCorrected = pitch - pitchOffset;
  float rollCorrected = roll - rollOffset;

  // Skalierung auf Joystickbereich (-32767 bis 32767)
  int16_t joyX = constrain(rollCorrected * (32767.0 / 45.0), -32767, 32767);
  int16_t joyY = constrain(pitchCorrected * (32767.0 / 45.0), -32767, 32767);

      Serial.print("JoyX: ");
    Serial.print(joyX);
    Serial.print(" JoyY: ");
    Serial.println(joyY);

  bleGamepad.setAxes(joyX, joyY, 0, 0, 0, 0);

  delay(20);  // 50 Hz
}
