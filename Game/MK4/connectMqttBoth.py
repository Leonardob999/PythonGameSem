import json
import paho.mqtt.client as mqtt

# Spieler 1 Daten
player1_data = {
    "ax": 0, "ay": 0, "az": 0,
    "gx": 0, "gy": 0, "gz": 0,
    "t": 0
}

# Spieler 2 Daten
player2_data = {
    "ax": 0, "ay": 0, "az": 0,
    "gx": 0, "gy": 0, "gz": 0,
    "t": 0
}

# Funktion zur Verarbeitung empfangener MQTT-Nachrichten
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        ax_value = data.get("ax")
        ay_value = data.get("ay")
        az_value = data.get("az")

        gx_value = data.get("gx")
        gy_value = data.get("gy")
        gz_value = data.get("gz")

        t_value = data.get("t")

        if ax_value is not None:
            if "player1" in msg.topic:
                player1_data["ax"] = ax_value
                player1_data["ay"] = ay_value
                player1_data["az"] = az_value
                player1_data["gx"] = gx_value
                player1_data["gy"] = gy_value
                player1_data["gz"] = gz_value
                player1_data["t"] = t_value

                print(f"[Player 1] ax={ax_value}, ay={ay_value}, az={az_value}, gx={gx_value}, gy={gy_value}, gz={gz_value}, temperature={t_value}")

            elif "player2" in msg.topic:
                player2_data["ax"] = ax_value
                player2_data["ay"] = ay_value
                player2_data["az"] = az_value
                player2_data["gx"] = gx_value
                player2_data["gy"] = gy_value
                player2_data["gz"] = gz_value
                player2_data["t"] = t_value

                print(f"[Player 2] ax={ax_value}, ay={ay_value}, az={az_value}, gx={gx_value}, gy={gy_value}, gz={gz_value}, temperature={t_value}")
        else:
            print("JSON-Objekt enthält keine ax-Daten.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")


# MQTT-Client einrichten
client = mqtt.Client()
client.on_message = on_message

broker_address = "85.215.147.207"  # Beispiel-Broker
client.connect(broker_address)

# Beide Topics abonnieren
client.subscribe("test/koordinaten/player1")
client.subscribe("test/koordinaten/player2")

client.loop_start()
print("Mit MQTT-Broker verbunden und auf Nachrichten von Spieler 1 & 2 wartend...")
