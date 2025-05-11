import pygame
import sys
from network import Network
from player import Player

class GameClient:
    def __init__(self, mode):
        """Initialisiert den Spiel-Client."""
        self.mode = mode
        self.win_width = 1000
        self.win_height = 1000
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Pong")

        # Initialisieren
        pygame.init()
        pygame.joystick.init()

        self.controller = None
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
        else:
            print("Kein Controller gefunden. Spiel wird mit Tastatur gespielt.")

        # Netzwerkverbindung und Spielvariablen
        self.network = Network()
        self.player = self.network.getP()  # Aktueller Spieler
        self.ball = None
        self.scores = [0, 0]  # Punktestand
        self.run = True

        if not isinstance(self.player, Player):  # Initialisieren des Spielers prüfen
            print("Fehler: Ungültige Daten vom Server erhalten!")
            self.close_game()

    def draw_scores(self):
        """Zeichnet die Punktestände."""
        font = pygame.font.SysFont("comicsans", 50)
        score_text = font.render(f"{self.scores[0]} - {self.scores[1]}", 1, (255, 255, 255))
        self.win.blit(score_text, (self.win_width // 2 - score_text.get_width() // 2, 20))

    def redraw_window(self, opponent, ball):
        """Grafik des Spielfensters aktualisieren."""
        self.win.fill((0, 0, 0))
        self.player.draw(self.win)
        opponent.draw(self.win)
        ball.draw(self.win)
        self.draw_scores()
        pygame.display.update()

    def display_game_over(self, message):
        """Anzeige für Spielende."""
        font = pygame.font.SysFont("comicsans", 80)
        button_font = pygame.font.SysFont("comicsans", 50)
        self.win.fill((0, 0, 0))
        text = font.render(message, 1, (255, 255, 255))
        self.win.blit(text, (self.win_width // 2 - text.get_width() // 2, self.win_height // 2 - text.get_height() // 2 - 50))

        button_color = (100, 100, 255)
        button_rect = pygame.Rect(self.win_width // 2 - 100, self.win_height // 2 + 50, 200, 80)
        pygame.draw.rect(self.win, button_color, button_rect)
        button_text = button_font.render("Zurück", 1, (0, 0, 0))
        self.win.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                    button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        return

    def handle_events(self):
        """Ereignisse wie Tastatureingaben und Controllerbewegungen verarbeiten."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                self.network.send("disconnect")

    def game_loop(self):
        """Die Hauptspielschleife."""
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(60)
            try:
                # Spielerbewegung und Empfang von Daten
                self.player.move(self.controller)
                data = self.network.send(self.player)

                if data is None:
                    print("Keine Daten erhalten, Spiel beenden.")
                    self.network.send("disconnect")
                    break

                opponent, self.ball, self.scores, game_over = data

                if game_over:
                    self.network.send("disconnect")
                    self.display_game_over(game_over)
                    self.run = False
                    break
            except Exception as e:
                print(f"Verbindungsfehler: {e}")
                self.network.send("disconnect")
                break

            # Ereignisse prüfen
            self.handle_events()

            # Fenster aktualisieren
            if self.ball and opponent:
                self.redraw_window(opponent, self.ball)

        self.close_game()

    def close_game(self):
        """Spiel sauber beenden."""
        pygame.quit()
        sys.exit()

    def start(self):
        """Startet den Spiel-Client."""
        print(f"Starte Spielmodus: {self.mode}")
        self.game_loop()


# Hauptaufruf
if __name__ == "__main__":
    if len(sys.argv) > 1:
        modus = sys.argv[1]
    else:
        modus = "default"  # Fallback-Spielmodus

    game_client = GameClient(modus)
    game_client.start()