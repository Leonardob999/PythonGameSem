import pickle
import json
import pygame
import sys
from serverClass import GameServer
from network import Network
import threading
import time
from helper import *  # Importiere das Shop-Menü aus helper.py
from client import Client

pygame.init()
pygame.mixer.init()  # Initialisiert den Soundmixer

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
        "ball_radius": 30,
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
    client = Client()
    client.start()

    print("gameclinet wurde gestartet")

def host_menu():
    """Menü für die Auswahl eines Spielmodus."""
    run = True
    while run:
        # Bildschirm aktualisieren
        win.fill(BLACK)

        # Schaltflächen zeichnen
        infinite_mode_button = draw_button(win, "Infinite Mode", WIN_WIDTH // 2 - 150, 250, 350, 80)
        best_of_7_button = draw_button(win, "Best of 7", WIN_WIDTH // 2 - 150, 350, 350, 80)
        gauntlet_mode_button = draw_button(win, "Gauntlet Mode", WIN_WIDTH // 2 - 150, 450, 350, 80)
        back_button = draw_button(win, "Zurück", WIN_WIDTH // 2 - 150, 550, 350, 80)

        # Ereignisse behandeln
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if infinite_mode_button.collidepoint(event.pos):
                    # Starte "Infinite Mode"
                    start_game(GAME_MODE_PRESETS[0])  # Spielmodus "infinite" starten
                    run = False  # Menü beenden
                elif best_of_7_button.collidepoint(event.pos):
                    # Starte "Best of 7"
                    start_game(GAME_MODE_PRESETS[1])  # Spielmodus "best_of_7" starten
                    run = False  # Menü beenden
                elif gauntlet_mode_button.collidepoint(event.pos):
                    # Starte "Gauntlet Mode"
                    start_game(GAME_MODE_PRESETS[2])  # Spielmodus "gauntlet" starten
                    run = False  # Menü beenden
                elif back_button.collidepoint(event.pos):
                    run = False  # Zurück zum Hauptmenü

                # Mauspositionen für Hover-Effekte
                mouse_pos = pygame.mouse.get_pos()
                draw_button(win, "Infinite Mode", WIN_WIDTH // 2 - 150, 250, 350, 80,
                            infinite_mode_button.collidepoint(mouse_pos))
                draw_button(win, "Best of 7", WIN_WIDTH // 2 - 150, 350, 350, 80,
                            best_of_7_button.collidepoint(mouse_pos))
                draw_button(win, "Gauntlet Mode", WIN_WIDTH // 2 - 150, 450, 350, 80,
                            gauntlet_mode_button.collidepoint(mouse_pos))
                draw_button(win, "Zurück", WIN_WIDTH // 2 - 150, 550, 350, 80,
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
        with open("Game/MK5/shop_data.json", "r") as f:
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