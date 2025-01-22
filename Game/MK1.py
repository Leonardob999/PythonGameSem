import tkinter as tk
from tkinter import ttk

import Game.connectMqtt as Mqtt

Mqtt.connect_to_mqtt()

x_scale = 3
y_scale = 3

root = tk.Tk()
root.title("Pong")

field = tk.Canvas(root, width=1000, height=1000)
rect = field.create_rectangle(10, 20, 30, 40)
field.grid(row=0, column=0)

rect1 = field.create_rectangle(10, 20, 30, 40)

def update():
    print("update")
    field.move(rect, Mqtt.x_data[0] * x_scale, Mqtt.y_data[0] * y_scale)
    root.after(20, update)

root.after(20, update)

# Tkinter-Hauptschleife starten
root.mainloop()