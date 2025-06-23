import pickle
import json
import os
import pygame
import sys
from serverClass import GameServer
from network import Network
import threading
import time
from helper import *  # Importiere das Shop-Menü aus helper.py
from client import Client





pygame.init()
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"[WARNUNG] Audio konnte nicht initialisiert werden: {e}")
    pygame.mixer = None  # Optional: deaktivieren

# Fenstergröße festlegen
WIN_WIDTH, WIN_HEIGHT = 1000, 800
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Hauptmenü")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)

# Schriftart
font = pygame.font.SysFont("comicsans", 50)

# Modus-Presets (anpassbare Werte)
GAME_MODE_PRESETS = [
    {
        "name": "infinite",
        "player_speed": 9,
        "ball_radius": 7,
        "max_score": None  # Unendlich
    },
    {
        "name": "best_of_7",
        "player_speed": 1,
        "max_score": 4  # 4 Siege für den Gewinn
    },
    {
        "name": "gauntlet",
        "player_speed": 7,
        "max_score": 7  # Spieler muss 7 Siege schaffen
    }
]


def draw_button(win, text, x, y, w, h, is_hovered=False):
    """Zeichnet eine Schaltfläche."""
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(win, color, (x, y, w, h))
    label = font.render(text, 1, BLACK)
    win.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)


def start_game(mode):
    print("gameclinet wird gestartet")
    server = GameServer(mode)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    time.sleep(0.1)
    client = Client(server=server, server_thread=server_thread)
    client.start()

    print("gameclinet wurde gestartet")

def format_mode_name(name):
    return name.replace("_", " ").title()

def host_menu():
    """Menü für die Auswahl eines Spielmodus."""
    BUTTON_WIDTH = 350
    BUTTON_HEIGHT = 80
    BUTTON_X = WIN_WIDTH // 2 - 150
    BUTTON_Y_START = 250
    BUTTON_Y_SPACING = 100
    run = True
    while run:
        # Bildschirm aktualisieren
        win.fill(BLACK)
        # Buttons erstellen & zeichnen
        mode_buttons = []
        for i, preset in enumerate(GAME_MODE_PRESETS):
            display_name = format_mode_name(preset["name"])
            y = BUTTON_Y_START + i * BUTTON_Y_SPACING
            button_rect = draw_button(win, display_name, BUTTON_X, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            mode_buttons.append((button_rect, preset))

        # Back-Button
        back_button_y = BUTTON_Y_START + len(GAME_MODE_PRESETS) * BUTTON_Y_SPACING
        back_button = draw_button(win, "Zurück", BUTTON_X, back_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Ereignisse behandeln
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, preset in mode_buttons:
                    if button_rect.collidepoint(event.pos):
                        start_game(preset)
                        run = False  # Menü beenden
                        break
                else:
                    if back_button.collidepoint(event.pos):
                        run = False  # Zurück zum Hauptmenü

            # Mauspositionen für Hover-Effekte
            mouse_pos = pygame.mouse.get_pos()
            for i, (button_rect, preset) in enumerate(mode_buttons):
                display_name = format_mode_name(preset["name"])
                y = BUTTON_Y_START + i * BUTTON_Y_SPACING
                draw_button(win, display_name, BUTTON_X, y, BUTTON_WIDTH, BUTTON_HEIGHT,
                            button_rect.collidepoint(mouse_pos))
            draw_button(win, "Zurück", BUTTON_X, back_button_y, BUTTON_WIDTH, BUTTON_HEIGHT,
                        back_button.collidepoint(mouse_pos))

        pygame.display.update()

def server_selection():
    """Menü für das beitreten zu einem server"""

    run = True
    while run:
        # Bildschirm aktualisieren
        win.fill(BLACK)

        ip_l = "100.101.29.26"  # IP für linken Button
        ip_r = "100.103.224.2"

        # Schaltflächen zeichnen
        join_server_button_l = draw_button(win, "100.101.29.26", WIN_WIDTH // 2 - 450/2, 250, 450, 80)
        join_server_button_r = draw_button(win, "100.103.224.2", WIN_WIDTH // 2 - 450/2, 350, 450, 80)
        back_button = draw_button(win, "Zurück", WIN_WIDTH // 2 - 150, 550, 350, 80)

        # Ereignisse behandeln
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if join_server_button_l.collidepoint(event.pos):
                    join_server(ip_l)
                if join_server_button_r.collidepoint(event.pos):
                    join_server(ip_r)
                elif back_button.collidepoint(event.pos):
                    run = False  # Zurück zum Hauptmenü

        # Mauspositionen für Hover-Effekte
        mouse_pos = pygame.mouse.get_pos()
        draw_button(win, "Lennart's Server Beitreten", WIN_WIDTH // 2 - 450/2, 250, 450, 80,
                    join_server_button_l.collidepoint(mouse_pos))

        draw_button(win, "Robin's Server Beitreten", WIN_WIDTH // 2 - 450/2, 350, 450, 80,
                    join_server_button_r.collidepoint(mouse_pos))

        draw_button(win, "Zurück", WIN_WIDTH // 2 - 150, 550, 350, 80,
                    back_button.collidepoint(mouse_pos))

        pygame.display.update()

def join_server(ip_address):
    # Hier musst du deine Netzwerkverbindung initialisieren,
    # z.B. indem du die IP weitergibst:
    client = Client(ip_address)  # verwende den Port wie benötigt
    client.start()


def main_menu():
    """Hauptmenü-Funktion."""
    run = True
    while run:

        path = get_path("Game/MK5/shop_data.json")
        default_data = {
            "owned_backgrounds": [0],
            "selected_background": 0,
            "owned_songs": [0],
            "selected_song": 0,
            "music_volume": 0.5,
            "xp": 0
        }

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    shop_data = json.load(f)
                    if not shop_data:  # Falls Datei leer ist (leeres dict)
                        shop_data = default_data
            except json.JSONDecodeError:
                shop_data = default_data
        else:
            shop_data = default_data

        def lade_shop_daten():
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
            else:
                data = {}

            # Standardwerte setzen
            data.setdefault("soundfx_on", True)

            return data

        # Fehlende Keys ergänzen (optional, falls schon Daten da sind)
        for key, val in default_data.items():
            if key not in shop_data:
                shop_data[key] = val

        with open(path, "w") as f:
            json.dump(shop_data, f, indent=4)

        # Bildschirm aktualisieren
        win.fill(BLACK)

        # Hauptschaltflächen zeichnen und den Variablen zuweisen
        host_button = draw_button(win, "Spiel hosten", WIN_WIDTH // 2 - 150, 200, 350, 80)
        join_button = draw_button(win, "Spiel beitreten", WIN_WIDTH // 2 - 150, 300, 350, 80)
        settings_button = draw_button(win, "Einstellungen", WIN_WIDTH // 2 - 150, 400, 350, 80)
        shop_button = draw_button(win, "Shop", WIN_WIDTH // 2 - 150, 500, 350, 80)
        quit_button = draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 600, 350, 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if host_button.collidepoint(event.pos):
                    host_menu()  # Zu den Spielmodi wechseln
                elif join_button.collidepoint(event.pos):
                    server_selection() #zur server selektion
                elif settings_button.collidepoint(event.pos):
                    einstellungen_menu()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif shop_button.collidepoint(event.pos):
                    shop_menu()  # Öffnet das Shop-Menü

        mouse_pos = pygame.mouse.get_pos()

        buttons = [
            ("Spiel hosten", host_button),
            ("Spiel beitreten", join_button),
            ("Einstellungen", settings_button),
            ("Shop", shop_button),
            ("Spiel beenden", quit_button)
        ]
        y_positions = [200, 300, 400, 500, 600]

        for (text, button), y in zip(buttons, y_positions):
            hovered = button.collidepoint(mouse_pos)
            draw_button(win, text, WIN_WIDTH // 2 - 150, y, 350, 80, hovered)


        # shop_data laden
        with open(get_path("Game/MK5/shop_data.json"), "r") as f:
            shop_data = json.load(f)

        # XP aus den Daten holen (z.B. 'winner_xp' oder dein tatsächlicher XP-Wert)
        xp_amount = shop_data.get("xp", 0)  # oder shop_data.get("total_xp", 0), je nach Struktur

        # Schriftart für die XP-Anzeige
        xp_font = pygame.font.SysFont("arial", 30)  # Schriftart und Größe definieren

        # Position der Anzeige
        xp_label = xp_font.render(f"XP: {xp_amount}", True, (255, 255, 255))
        xp_x = WIN_WIDTH // 2 - xp_label.get_width() // 2  # Zentriert oben mittig
        xp_y = 20  # Abstand vom oberen Rand

        # Zeichne den Text im Hauptbereich (z. B. im main_menu())
        win.blit(xp_label, (xp_x, xp_y))
        pygame.display.update()



if __name__ == "__main__":
    main_menu()