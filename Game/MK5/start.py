import pygame
import sys
from helper import *  # Importiere das Shop-Menü aus helper.py
from Game.MK5.client import GameClient

pygame.init()

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
        "ball_speed": 4,
        "player_speed": 6,
        "max_score": None  # Unendlich
    },
    {
        "name": "best_of_7",
        "ball_speed": 5,
        "player_speed": 6,
        "max_score": 4  # 4 Siege für den Gewinn
    },
    {
        "name": "gauntlet",
        "ball_speed": 6,
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
    """Erstellt und startet ein GameClient-Objekt. Der Modus kann None sein."""
    if mode is not None:  # Spielmodus
        print("mode")
        game_client = GameClient(mode)
    else:  # Nur Verbindung herstellen
        print("Tritt Spiel bei...")
        game_client = GameClient(None)
    game_client.start()
    print("gameclinet wurde gestartet")

def game_mode_menu():
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


def main_menu():
    """Hauptmenü-Funktion."""
    run = True
    while run:
        # Bildschirm aktualisieren
        win.fill(BLACK)

        # Hauptschaltflächen zeichnen
        start_button = draw_button(win, "Spiel starten", WIN_WIDTH // 2 - 150, 300, 350, 80)
        settings_button = draw_button(win, "Einstellungen", WIN_WIDTH // 2 - 150, 400, 350, 80)
        quit_button = draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 600, 350, 80)
        shop_button = draw_button(win, "Shop", WIN_WIDTH // 2 - 150, 500, 350, 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_mode_menu()  # Zu den Spielmodi wechseln
                elif settings_button.collidepoint(event.pos):
                    einstellungen_menu()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif shop_button.collidepoint(event.pos):
                    shop_menu()  # Öffnet das Shop-Menü

        mouse_pos = pygame.mouse.get_pos()
        draw_button(win, "Spiel starten", WIN_WIDTH // 2 - 150, 300, 350, 80, start_button.collidepoint(mouse_pos))
        draw_button(win, "Einstellungen", WIN_WIDTH // 2 - 150, 400, 350, 80, settings_button.collidepoint(mouse_pos))
        draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 600, 350, 80, quit_button.collidepoint(mouse_pos))
        draw_button(win, "Shop", WIN_WIDTH // 2 - 150, 500, 350, 80, shop_button.collidepoint(mouse_pos))

                # Beispielwerte für das Design
        level = 7         # aktuelles Level
        current_xp = 300  # aktuelle XP
        needed_xp = 500   # XP fürs nächste Level

        # Größe des Balkens
        bar_width = 400
        bar_height = 36

        # Y-Position kannst du bei Bedarf noch anpassen!
        bar_y = 120

        # ---- Zentrale Berechnung: absolute Mitte der XP-Bar ----
        center_x = WIN_WIDTH // 2
        bar_x = center_x - bar_width // 2

        # Balken-Hintergrund (grau)
        pygame.draw.rect(win, (120, 120, 120), (bar_x, bar_y, bar_width, bar_height), border_radius=12)
        # Balken-Füllung je nach Fortschritt (blaugrün)
        progress = min(current_xp / needed_xp, 1.0)
        fill_width = int(bar_width * progress)
        pygame.draw.rect(win, (60, 180, 220), (bar_x, bar_y, fill_width, bar_height), border_radius=12)
        # Optional: leichte Umrandung
        pygame.draw.rect(win, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height), 3, border_radius=12)

        # Level-Zahl drüber malen (mittig zu XP-Bar)
        level_font = pygame.font.SysFont("comicsans", 34, True)
        level_label = level_font.render(f"Level {level}", True, (250, 230, 80))
        level_label_x = center_x - level_label.get_width() // 2
        win.blit(level_label, (level_label_x, bar_y - 42))

        # XP-Fortschritt als Text auf Balken (mittig zu XP-Bar)
        xp_font = pygame.font.SysFont("comicsans", 22, bold=True)
        xp_label = xp_font.render(f"{current_xp} / {needed_xp} XP", True, (240,240,255))
        xp_label_x = center_x - xp_label.get_width() // 2
        xp_label_y = bar_y + bar_height//2 - xp_label.get_height()//2
        win.blit(xp_label, (xp_label_x, xp_label_y))

        pygame.display.update()


if __name__ == "__main__":
    main_menu()