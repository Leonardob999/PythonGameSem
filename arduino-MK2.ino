#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// MPU6050-Objekt
Adafruit_MPU6050 mpu;

// WLAN- und MQTT-Konfiguration
const char* ssid = "IPAD";                      // schule: IPAD
const char* password = "Fri3drich3bert5chul3";  // schule: Fri3drich3bert5chul3
const char* mqtt_server = "85.215.147.207";     // Beispiel-MQTT-Broker
const char* topic = "test/koordinaten";

WiFiClient espClient;
PubSubClient client(espClient);

// Bias-Werte zur Driftkorrektur (empirisch ermittelt oder kalibriert)
const float bias_x = 0.01;  // Beispielhafte Driftkorrekturwerte
const float bias_y = 0.01;

unsigned long lastTime = 0;
const unsigned long interval = 10;  // Sendeintervall in ms (anpassbar)

// Setup
void setup() {
  Serial.begin(115200);
  Wire.begin(7, 6);

  // MPU6050 initialisieren
  if (!mpu.begin()) {
    Serial.println("MPU6050-Verbindung fehlgeschlagen!");
    while (1)
      ;  // Endlos-Schleife bei Fehler
  } else {
    Serial.println("MPU6050 verbunden!");
  }

  // MPU6050 konfigurieren
  mpu.setHighPassFilter(MPU6050_HIGHPASS_5_HZ);  // Höherer Wert zur besseren Driftunterdrückung
  mpu.setMotionDetectionThreshold(1);
  mpu.setMotionDetectionDuration(20);
  mpu.setInterruptPinLatch(true);
  mpu.setInterruptPinPolarity(true);
  mpu.setMotionInterrupt(true);

  // WLAN verbinden
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWLAN verbunden!");

  // MQTT-Client konfigurieren
  client.setServer(mqtt_server, 1883);
  reconnectMQTT();
}

// Hauptschleife
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  unsigned long currentTime = millis();

  if (currentTime - lastTime >= interval) {
    lastTime = currentTime;

    // Sensor-Daten vom MPU6050 lesen
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Driftkorrigierte Beschleunigungswerte berechnen
    float correctedX = g.gyro.x - bias_x;
    float correctedY = g.gyro.y - bias_y;

    // JSON-Daten erstellen und senden
    sendData(correctedX, correctedY);

    Serial.print("X: ");
    Serial.print(correctedX);
    Serial.print(" Y: ");
    Serial.println(correctedY);
  }
}

// Funktion zum Senden der Daten über MQTT
void sendData(float x, float y) {
  // JSON-Objekt erstellen
  StaticJsonDocument<200> doc;
  doc["x"] = x;
  doc["y"] = y;

  char buffer[256];
  size_t n = serializeJson(doc, buffer);

  // JSON-Daten über MQTT senden
  if (client.publish(topic, buffer, n)) {
    Serial.println("JSON-Daten gesendet:");
    Serial.println(buffer);
  } else {
    Serial.println("Fehler beim Senden der JSON-Daten.");
  }
}

// Funktion zur Wiederverbindung mit dem MQTT-Broker
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Verbindung mit MQTT-Broker wird hergestellt...");
    if (client.connect("ESP32Client")) {
      Serial.println("Verbunden!");
    } else {
      Serial.print("Fehler, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}
