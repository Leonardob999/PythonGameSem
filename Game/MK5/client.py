import pygame
from network import Network


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


# Soundeffekt lokal laden (nur im Client verwenden)
bounce_sound = pygame.mixer.Sound("Game/MK5/sounds/bounce.wav")


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


def main():
    run = True
    clock = pygame.time.Clock()

    # Netzwerkverbindung zum Server
    n = Network()

    # Spieler- und Balldaten vom Server erhalten
    player = n.getP()  # Aktueller Spieler
    ball = n.getB()  # Der Ball
    scores = [0, 0]  # Initialer Punktestand

    # Prüfe, ob Daten gültig sind
    if player is None or ball is None:
        print("Failed to receive initial data from server!")
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
                break

            # Daten vom Server entpacken
            opponent = data[0]  # Gegenspieler
            ball = data[1]  # Ball
            scores = data[2]  # Punktestand

            # Sound abspielen, wenn der Ball etwas trifft
            if ball.vel_x < 0 or ball.vel_y < 0:  # Simplifiziertes Beispiel
                bounce_sound.play()

        except Exception as e:
            print(f"Connection error: {e}")
            break

        # Spiel beenden, wenn ESCAPE gedrückt wird
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Spielfenster aktualisieren
        if ball and opponent:  # Überprüfen, ob gültige Objekte vorhanden sind
            redraw_window(win, player, opponent, ball, scores)
        else:
            print("Invalid game state, objects missing!")
            break

    pygame.quit()


# Hauptfunktion starten
if __name__ == "__main__":
    main()
