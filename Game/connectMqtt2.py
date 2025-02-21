import json
import paho.mqtt.client as mqtt

# Global variables for received sensor data
a_x_data = 0
a_y_data = 0
a_z_data = 0

g_x_data = 0
g_y_data = 0
g_z_data = 0

temperature = 0

# MQTT Broker details
broker_address = "85.215.147.207"
topic = "test/koordinaten/1"

# Function to process incoming MQTT messages
def on_message(client, userdata, msg):
    global a_x_data, a_y_data, a_z_data, g_x_data, g_y_data, g_z_data, temperature
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)  # Convert JSON to dictionary

        # Extract values from JSON
        a_x_data = data.get("ax", 0)
        a_y_data = data.get("ay", 0)
        a_z_data = data.get("az", 0)

        g_x_data = data.get("gx", 0)
        g_y_data = data.get("gy", 0)
        g_z_data = data.get("gz", 0)

        temperature = data.get("t", 0)

        print(f"📩 Received: ax={a_x_data}, ay={a_y_data}, az={a_z_data}, gx={g_x_data}, gy={g_y_data}, gz={g_z_data}, temp={temperature}")

    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

# Function to handle successful MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker!")
        client.subscribe(topic)
    else:
        print(f"❌ Connection failed, error code {rc}")

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

print("🔄 Connecting to MQTT broker...")
client.connect(broker_address)

# Start the MQTT loop in the background
client.loop_start()
print("📡 Listening for incoming messages...")
