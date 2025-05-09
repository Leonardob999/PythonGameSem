import pygame
from network import Network
from player import Player
import start

# Fenstergröße festlegen
WIN_WIDTH, WIN_HEIGHT = 1000, 1000
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong")

# Pygame initialisieren
pygame.init()

# Controller initialisieren
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None
    print("Kein Controller gefunden. Spiel wird mit Tastatur gespielt.")



# Punktestand zeichnen
def draw_scores(win, scores):
    font = pygame.font.SysFont("comicsans", 50)  # Schriftart festlegen
    score_text = font.render(f"{scores[0]} - {scores[1]}", 1, (255, 255, 255))  # Punktestand rendern
    win.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, 20))  # Punktestand zentriert oben anzeigen


# Spiellogik für die Anzeige
def redraw_window(win, player1, player2, ball, scores):
    win.fill((0, 0, 0))  # Bildschirm schwarz löschen

    # Spieler, Ball und Punktestand zeichnen
    player1.draw(win)
    player2.draw(win)
    ball.draw(win)
    draw_scores(win, scores)

    pygame.display.update()  # Aktualisiert das Fenster


def display_game_over(win, message):
    font = pygame.font.SysFont("comicsans", 80)
    button_font = pygame.font.SysFont("comicsans", 50)
    win.fill((0, 0, 0))  # Bildschirm leeren

    # Gewinnmitteilung
    text = font.render(message, 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, WIN_HEIGHT // 2 - text.get_height() // 2 - 50))

    # "Zurück"-Button
    button_color = (100, 100, 255)
    button_rect = pygame.Rect(WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 + 50, 200, 80)
    pygame.draw.rect(win, button_color, button_rect)
    button_text = button_font.render("Zurück", 1, (0, 0, 0))
    win.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                           button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))

    pygame.display.update()

    # Button-Logik
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    return  # Zurück zum Start

def main():
    run = True
    clock = pygame.time.Clock()

    # Netzwerkverbindung zum Server
    n = Network()

    # Spieler- und Balldaten vom Server erhalten
    player = n.getP()  # Aktueller Spieler
    ball = n.getB()  # Der Ball
    scores = [0, 0]  # Initialer Punktestand

    if not isinstance(player, Player):  # Prüfen, ob ein gültiger Spieler-Objekt erhalten wurde
        print("Failed to receive valid initial data from server!")
        return

    while run:
        clock.tick(60)

        try:
            # Spielerbewegung senden und Daten vom Server empfangen
            player.move(controller)
            data = n.send(player)

            # Verifiziere, dass Daten nicht None sind
            if data is None:
                print("No data received from server. Closing connection.")
                n.send("disconnect")
                break

            # Daten vom Server entpacken
            opponent = data[0]  # Gegenspieler
            ball = data[1]  # Ball
            scores = data[2]  # Punktestand
            game_over = data[3]  # Spielstatus

            if game_over:  # Wenn das Spiel vorbei ist
                n.send("disconnect")  # Verbindung beenden
                display_game_over(win, game_over)
                run = False  # Verbindung beenden und Schleife abbrechen
                break
        except Exception as e:
            print(f"Connection error: {e}")
            n.send("disconnect")
            break

        # Spiel beenden, wenn ESCAPE gedrückt wird
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                n.send("disconnect")  # Verbindung sauber beenden
                break

        # Spielfenster aktualisieren
        if ball and opponent:  # Überprüfen, ob gültige Objekte vorhanden sind
            redraw_window(win, player, opponent, ball, scores)
        else:
            print("Invalid game state, objects missing!")
            break

    # Spiel sauber beenden und zum Startbildschirm zurückkehren
    pygame.quit()

    # Hier sicherstellen, dass kein "game_over"-Message mehr angezeigt wird
    main_screen = start.main()  # Starte den Startbildschirm erneut




# Hauptfunktion starten
if __name__ == "__main__":
    main()