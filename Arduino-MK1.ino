#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// MPU6050-Objekt
Adafruit_MPU6050 mpu;

// WLAN- und MQTT-Konfiguration
const char* ssid = "IPAD";
const char* password = "Fri3drich3bert5chul3";
const char* mqtt_server = "85.215.147.207";  // Beispiel-MQTT-Broker
const char* topic = "test/koordinaten";

WiFiClient espClient;
PubSubClient client(espClient);

// Variablen zur Berechnung
float prev_x = 0, prev_y = 0;
unsigned long lastTime = 0;
const unsigned long interval = 10;  // Sendeintervall in ms (anpassbar)

// Setup
void setup() {
  Serial.begin(115200);
  Wire.begin(7, 6);

  // MPU6050 initialisieren
  if (!mpu.begin()) {
    Serial.println("MPU6050-Verbindung fehlgeschlagen!");
    while (1); // Endlos-Schleife bei Fehler
  } else {
    Serial.println("MPU6050 verbunden!");
  }

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

    float a_x = a.acceleration.x;
    float a_y = a.acceleration.y;
    float a_z = a.acceleration.z;

    float g_x = g.gyro.x;
    float g_y = g.gyro.y;
    float g_z = g.gyro.z;

    float t = temp.temperature;


    // JSON-Daten erstellen
    sendData(a_x, a_y, a_z, g_x, g_y, g_z, t);

    Serial.print("gx: "); Serial.print(a_x);
    Serial.print("gy: "); Serial.println(g_x);
  }
}

// Funktion zum Senden der Daten über MQTT
void sendData(float ax, float ay, float az, float gx, float gy, float gz, float t) {
  // JSON-Objekt erstellen
  StaticJsonDocument<200> doc;
  doc["ax"] = ax;
  doc["ay"] = ay;
  doc["az"] = az;
  doc["gx"] = gx;
  doc["gy"] = gy;
  doc["gz"] = gz;
  doc["t"] = t;

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
