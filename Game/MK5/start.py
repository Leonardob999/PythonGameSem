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
GAME_MODE_PRESETS = {
    "infinite": {
        "ball_speed": 4,
        "player_speed": 6,
        "max_score": None  # Unendlich
    },
    "best_of_7": {
        "ball_speed": 5,
        "player_speed": 6,
        "max_score": 4  # 4 Siege für den Gewinn
    },
    "gauntlet": {
        "ball_speed": 6,
        "player_speed": 7,
        "max_score": 7  # Spieler muss 7 Siege schaffen
    },
}

def draw_button(win, text, x, y, w, h, is_hovered=False):
    """Zeichnet eine Schaltfläche."""
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(win, color, (x, y, w, h))
    label = font.render(text, 1, BLACK)
    win.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)


def start_game(mode):
    """Erstellt und startet ein GameClient-Objekt. Der Modus kann None sein."""
    if mode is not None:  # Spielmodus
        presets = GAME_MODE_PRESETS.get(mode)
        print(f"Starte Spielmodus: {mode} mit Presets: {presets}")
        game_client = GameClient(mode, presets)
    else:  # Nur Verbindung herstellen
        print("Tritt Spiel bei...")
        game_client = GameClient(None, None)
    game_client.start()

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
                    start_game("infinite")  # Spielmodus "infinite" starten
                    run = False  # Menü beenden
                elif best_of_7_button.collidepoint(event.pos):
                    # Starte "Best of 7"
                    start_game("best_of_7")  # Spielmodus "best_of_7" starten
                    run = False  # Menü beenden
                elif gauntlet_mode_button.collidepoint(event.pos):
                    # Starte "Gauntlet Mode"
                    start_game("gauntlet")  # Spielmodus "gauntlet" starten
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
        quit_button = draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 500, 350, 80)
        shop_button = draw_button(win, "Shop", WIN_WIDTH // 2 - 150, 600, 350, 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_mode_menu()  # Zu den Spielmodi wechseln
                elif settings_button.collidepoint(event.pos):
                    print("Einstellungsmenü (noch zu implementieren)")
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif shop_button.collidepoint(event.pos):
                    shop_menu()  # Öffnet das Shop-Menü

        mouse_pos = pygame.mouse.get_pos()
        draw_button(win, "Spiel starten", WIN_WIDTH // 2 - 150, 300, 350, 80, start_button.collidepoint(mouse_pos))
        draw_button(win, "Einstellungen", WIN_WIDTH // 2 - 150, 400, 350, 80, settings_button.collidepoint(mouse_pos))
        draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 500, 350, 80, quit_button.collidepoint(mouse_pos))
        draw_button(win, "Shop", WIN_WIDTH // 2 - 150, 600, 350, 80, shop_button.collidepoint(mouse_pos))

        pygame.display.update()


if __name__ == "__main__":
    main_menu()