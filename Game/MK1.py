import tkinter as tk
from tkinter import ttk

import Game.connectMqtt as Mqtt

x_scale = 3
y_scale = 3

x = 0
y = 0

root = tk.Tk()
root.title("Pong")

field = tk.Canvas(root, width=1000, height=1000)
rect = field.create_rectangle(10, 20, 30, 40)
field.grid(row=0, column=0)

rect1 = field.create_rectangle(10, 20, 30, 40)

def updateVars():
    global x, y
    if Mqtt.x_data > 0.8 or Mqtt.x_data < 0:
        x = Mqtt.x_data

    if Mqtt.y_data > 0 or Mqtt.y_data < -0.4:
        y = Mqtt.y_data

def update():
    field.move(rect, x * x_scale, Mqtt.y_data * y_scale)
    root.after(20, update)

root.after(20, update)

# Tkinter-Hauptschleife starten
root.mainloop()