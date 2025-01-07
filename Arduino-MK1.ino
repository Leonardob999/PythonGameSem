#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <WiFi.h>
#include <PubSubClient.h>

// MPU6050-Objekt
Adafruit_MPU6050 mpu;

// WLAN- und MQTT-Konfiguration
const char* ssid = "IPAD";
const char* password = "Friedrich3bert5chul3";
const char* mqtt_server = "85.215.147.207";  // Beispiel-MQTT-Broker
const char* topic = "test/koordinaten";

WiFiClient espClient;
PubSubClient client(espClient);

// Arrays für X- und Y-Werte
const int dataSize = 500;  // 500 Werte für 5 Sekunden bei 100 Hz
float x[dataSize];
float y[dataSize];

// Variablen zur Berechnung
float prev_x = 0, prev_y = 0;
unsigned long lastTime = 0;
const unsigned long interval = 10;  // 10 ms Intervall für 100 Hz

int dataIndex = 0;  // Index für Arrays

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  // MPU6050 initialisieren
  if (!mpu.begin()) {
    Serial.println("MPU6050-Verbindung fehlgeschlagen!");
    while (1); // Warten, wenn die Verbindung fehlschlägt
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
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  unsigned long currentTime = millis();
  
  if (currentTime - lastTime >= interval && dataIndex < dataSize) {
    lastTime = currentTime;
    
    // Sensor-Daten vom MPU6050 lesen
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    // Relative Bewegung berechnen (vereinfachtes Beispiel)
    float deltaX = a.acceleration.x * 0.001;  // Skalierung anpassen
    float deltaY = a.acceleration.y * 0.001;
    
    // Auf letzten Wert aufaddieren
    prev_x += deltaX;
    prev_y += deltaY;
    
    // Werte in Arrays speichern
    x[dataIndex] = prev_x;
    y[dataIndex] = prev_y;
    dataIndex++;

    Serial.print("X: "); Serial.print(prev_x);
    Serial.print(" Y: "); Serial.println(prev_y);
  }

  // Nach 5 Sekunden Daten senden
  if (dataIndex >= dataSize) {
    sendData();
    dataIndex = 0;  // Arrays zurücksetzen
    prev_x = 0;
    prev_y = 0;
    delay(5000);  // Warte 5 Sekunden vor dem nächsten Zyklus
  }
}

// Funktion zum Senden der Daten über MQTT
void sendData() {
  String x_str = "", y_str = "";

  for (int i = 0; i < dataSize; i++) {
    x_str += String(x[i]);
    y_str += String(y[i]);
    if (i < dataSize - 1) {
      x_str += ",";
      y_str += ",";
    }
  }

  String payload = x_str + "|" + y_str;
  client.publish(topic, payload.c_str());
  Serial.println("Daten gesendet: ");
  Serial.println(payload);
}

// Funktion zur Wiederverbindung mit dem MQTT-Broker
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Verbindung mit MQTT-Broker wird hergestellt...");
    if (client.connect("ArduinoClient")) {
      Serial.println("Verbunden!");
      client.subscribe(topic);
    } else {
      Serial.print("Fehler, rc=");
      Serial.print(client.state());
      Serial.println(" Neuer Versuch in 5 Sekunden...");
      delay(5000);
    }
  }
}
