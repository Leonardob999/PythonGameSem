import json
import paho.mqtt.client as mqtt

# Arrays für empfangene Daten
x_data = []
y_data = []

# Funktion zur Verarbeitung empfangener MQTT-Nachrichten
def on_message(client, userdata, msg):
    global x_data, y_data
    try:
        # JSON-Daten dekodieren
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)  # JSON in ein Dictionary umwandeln

        # X- und Y-Werte aus JSON extrahieren
        x_value = data.get("x")
        y_value = data.get("y")

        if x_value is not None and y_value is not None:
            # Werte den globalen Arrays hinzufügen
            x_data.append(x_value)
            y_data.append(y_value)
            print(f"Empfangen: x={x_value}, y={y_value}")
        else:
            print("JSON-Objekt enthält keine x- oder y-Daten.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")


# MQTT-Client einrichten
client = mqtt.Client()
client.on_message = on_message

def connect_to_mqtt():
    broker_address = "85.215.147.207"  # Beispiel-Broker
    topic = "test/koordinaten"
    client.connect(broker_address)
    client.subscribe(topic)
    client.loop_start()  # Hintergrund-Thread starten
    print("Mit MQTT-Broker verbunden und auf Nachrichten wartend...")