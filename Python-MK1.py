import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import paho.mqtt.client as mqtt

# Arrays für empfangene Daten
x_data = []
y_data = []

# Funktion zur Verarbeitung empfangener MQTT-Nachrichten
def on_message(client, userdata, msg):
    global x_data, y_data
    try:
        # Nachricht in zwei Arrays umwandeln (z.B. "1,2,3,4|2,3,5,7")
        payload = msg.payload.decode("utf-8")
        x_str, y_str = payload.split('|')
        x_data = list(map(int, x_str.split(',')))
        y_data = list(map(int, y_str.split(',')))
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")

# MQTT-Client einrichten
client = mqtt.Client()
client.on_message = on_message

def connect_to_mqtt():
    broker_address = "broker.hivemq.com"  # Beispiel-Broker
    topic = "test/koordinaten"
    client.connect(broker_address)
    client.subscribe(topic)
    client.loop_start()  # Hintergrund-Thread starten
    print("Mit MQTT-Broker verbunden und auf Nachrichten wartend...")

# Funktion zum Plotten der empfangenen Punkte
def plot_points():
    global x_data, y_data
    if not x_data or not y_data:
        print("Noch keine Daten empfangen!")
        return

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x_data, y_data, marker='o', linestyle='-', color='b')
    ax.set_xlabel('X-Achse')
    ax.set_ylabel('Y-Achse')
    ax.set_title('MQTT-Daten im Koordinatensystem')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Hauptfenster erstellen
window = tk.Tk()
window.title("Koordinatensystem mit MQTT-Daten")

# Button zum Verbinden mit dem MQTT-Broker
connect_button = tk.Button(window, text="Mit MQTT verbinden", command=connect_to_mqtt)
connect_button.pack()

# Button zum Plotten der Punkte
plot_button = tk.Button(window, text="Plot erstellen", command=plot_points)
plot_button.pack()

# Tkinter-Hauptschleife starten
window.mainloop()