import json
import paho.mqtt.client as mqtt

# Arrays für empfangene Daten
a_x_data = 0
a_y_data = 0
a_z_data = 0

g_x_data = 0
g_y_data = 0
g_z_data = 0

temperature = 0

# Funktion zur Verarbeitung empfangener MQTT-Nachrichten
def on_message(client, userdata, msg):
    global a_x_data, a_y_data, a_z_data, g_x_data, g_y_data, g_z_data, temperature
    try:
        # JSON-Daten dekodieren
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)  # JSON in ein Dictionary umwandeln

        # X- und Y-Werte aus JSON extrahieren
        ax_value = data.get("ax")
        ay_value = data.get("ay")
        az_value = data.get("az")

        gx_value = data.get("gx")
        gy_value = data.get("gy")
        gz_value = data.get("gz")

        t_value = data.get("t")

        if ax_value is not None:
            # Werte den globalen Arrays hinzufügen
            a_x_data = ax_value
            a_y_data = ay_value
            a_z_data = az_value

            g_x_data = gx_value
            g_y_data = gy_value
            g_z_data = gz_value

            temperature = t_value
            print(f"Empfangen: ax={ax_value}, ay={ay_value}, az={az_value}, gx={gx_value}, gy={gy_value}, gz={gz_value}, temperature={t_value}")
        else:
            print("JSON-Objekt enthält keine x- oder y-Daten.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")


# MQTT-Client einrichten
client = mqtt.Client()
client.on_message = on_message


broker_address = "85.215.147.207"  # Beispiel-Broker
topic = "test/koordinaten"
client.connect(broker_address)
client.subscribe(topic)
client.loop_start()  # Hintergrund-Thread starten
print("Mit MQTT-Broker verbunden und auf Nachrichten wartend...")
