import pygame
import sys
from network import Network
from player import Player


class GameClient:
    def __init__(self, mode, presets):
        """Initialisiert den Spiel-Client. Modus und Presets können None sein."""
        self.mode = mode
        self.presets = presets
        self.win_width = 1000
        self.win_height = 800
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Pong")

        pygame.init()
        pygame.joystick.init()

        # Default-Werte für den Fall, dass keine Presets gesetzt sind
        if presets:
            self.ball_speed = presets.get("ball_speed", 5)  # Standardgeschwindigkeit
            self.player_speed = presets.get("player_speed", 5)
            self.max_score = presets.get("max_score", None)
        else:
            self.ball_speed = 5
            self.player_speed = 5
            self.max_score = None

        # Netzwerkverbindung
        self.network = Network()

        # Spielfortschritt
        self.run = True
        self.player = None
        self.ball = None
        self.scores = [0, 0]

    def start(self):
        """Startet den Spiel-Client."""
        print(f"Verbinde mit Spiel. Modus: {self.mode}, Presets: {self.presets}")
        self.game_loop()

    def game_loop(self):
        """Die Hauptspielschleife."""
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(60)  # 60 FPS

            try:
                # Netzwerkdaten laden
                data = self.network.send(self.player)  # Aktuellen Spielerstatus senden
                if data is None:
                    print("Keine Daten vom Server erhalten. Beende Spielschleife.")
                    self.run = False
                    break

                if isinstance(data, tuple):
                    self.player, self.ball, self.scores, game_over = data
                    print(f"Aktualisierte Daten: Player: {self.player}, Scores: {self.scores}, Ball: {self.ball}")
                    if game_over:
                        print(game_over)
                        self.run = False

                # Ereignisse prüfen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        self.network.send("disconnect")

                # Bildschirm aktualisieren
                self.win.fill((0, 0, 0))  # Schwarzer Hintergrund
                pygame.display.update()

            except Exception as e:
                print(f"Fehler in der Spielschleife: {e}")
                self.run = False
                self.network.send("disconnect")

        pygame.quit()
        print("Spiel beendet.")