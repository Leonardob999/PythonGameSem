import pygame
import sys
from game import start_game  # Importiere die `start_game`-Funktion aus der bestehenden Spiellogik

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


def draw_button(win, text, x, y, w, h, is_hovered=False):
    """Zeichnet eine Schaltfläche."""
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(win, color, (x, y, w, h))
    label = font.render(text, 1, BLACK)
    win.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)


def play_infinite_mode():
    """Startet den unendlichen Spielmodus."""
    start_game("infinite")  # Ruft die Spielfunktion mit Modus "infinite" auf


def play_best_of_7():
    """Startet den 'Best of 7'-Modus."""
    start_game("best_of_7")  # Ruft die Spielfunktion mit Modus "best_of_7" auf


def play_gauntlet_mode():
    """Startet den 'Gauntlet'-Modus."""
    start_game("gauntlet")  # Ruft die Spielfunktion mit Modus "gauntlet" auf


def game_mode_menu():
    """Menü für die Auswahl eines Spielmodus."""
    run = True
    while run:
        # Bildschirm aktualisieren
        win.fill(BLACK)

        # Schaltflächen zeichnen
        infinite_mode_button = draw_button(win, "Infinite Mode", WIN_WIDTH // 2 - 150, 300, 350, 80)
        best_of_7_button = draw_button(win, "Best of 7", WIN_WIDTH // 2 - 150, 400, 350, 80)
        gauntlet_mode_button = draw_button(win, "Gauntlet Mode", WIN_WIDTH // 2 - 150, 500, 350, 80)
        back_button = draw_button(win, "Zurück", WIN_WIDTH // 2 - 150, 600, 350, 80)

        # Ereignisse behandeln
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if infinite_mode_button.collidepoint(event.pos):
                    play_infinite_mode()
                    run = False  # Menü schließen, Spielmodus startet
                elif best_of_7_button.collidepoint(event.pos):
                    play_best_of_7()
                    run = False  # Menü schließen, Spielmodus startet
                elif gauntlet_mode_button.collidepoint(event.pos):
                    play_gauntlet_mode()
                    run = False  # Menü schließen, Spielmodus startet
                elif back_button.collidepoint(event.pos):
                    run = False  # Zurück zum Hauptmenü

        # Hover-Effekte
        mouse_pos = pygame.mouse.get_pos()
        draw_button(win, "Infinite Mode", WIN_WIDTH // 2 - 150, 300, 350, 80,
                    infinite_mode_button.collidepoint(mouse_pos))
        draw_button(win, "Best of 7", WIN_WIDTH // 2 - 150, 400, 350, 80,
                    best_of_7_button.collidepoint(mouse_pos))
        draw_button(win, "Gauntlet Mode", WIN_WIDTH // 2 - 150, 500, 350, 80,
                    gauntlet_mode_button.collidepoint(mouse_pos))
        draw_button(win, "Zurück", WIN_WIDTH // 2 - 150, 600, 350, 80, back_button.collidepoint(mouse_pos))

        pygame.display.update()


def main_menu():
    """Hauptmenü-Funktion."""
    run = True
    while run:
        # Bildschirm aktualisieren
        win.fill(BLACK)

        # Schaltflächen zeichnen
        start_button = draw_button(win, "Spiel starten", WIN_WIDTH // 2 - 150, 300, 300, 80)
        settings_button = draw_button(win, "Einstellungen", WIN_WIDTH // 2 - 150, 400, 300, 80)
        quit_button = draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 500, 300, 80)

        # Ereignisse behandeln
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_mode_menu()  # Zu den Spielmodi wechseln
                elif settings_button.collidepoint(event.pos):
                    settings_menu()  # (Platzhalter) Einstellungen öffnen
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Hover-Effekte
        mouse_pos = pygame.mouse.get_pos()
        draw_button(win, "Spiel starten", WIN_WIDTH // 2 - 150, 300, 350, 80, start_button.collidepoint(mouse_pos))
        draw_button(win, "Einstellungen", WIN_WIDTH // 2 - 150, 400, 350, 80, settings_button.collidepoint(mouse_pos))
        draw_button(win, "Spiel beenden", WIN_WIDTH // 2 - 150, 500, 350, 80, quit_button.collidepoint(mouse_pos))

        pygame.display.update()


def settings_menu():
    """Platzhalter für Einstellungen."""
    print("Einstellungsmenü (noch zu implementieren)")


if __name__ == "__main__":
    main_menu()
