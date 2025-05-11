import pygame
import sys
from network import Network
from player import Player


class GameClient:
    def __init__(self, mode, presets):
        """Initialisiert den Spiel-Client mit übergebenen Presets."""
        self.mode = mode
        self.presets = presets  # Erhalte die Modus-Presets
        self.win_width = 1000
        self.win_height = 1000
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Pong")

        pygame.init()
        pygame.joystick.init()

        # Einstellungen aus Presets
        self.ball_speed = self.presets["ball_speed"]
        self.player_speed = self.presets["player_speed"]
        self.max_score = self.presets.get("max_score", None)

        # Netzwerkverbindung und Spielvariablen
        self.network = Network()
        self.player = None
        self.ball = None
        self.scores = [0, 0]  # Punktestand
        self.run = True

    def start(self):
        """Startet den Spiel-Client."""
        print(f"Starte Spielmodus: {self.mode}")
        self.game_loop()  # Ruft die Hauptspielschleife auf

    def game_loop(self):
        """Die Hauptspielschleife."""
        # Beispielinhalt (kann durch deine Spiellogik ersetzt oder ergänzt werden)
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(60)
            try:
                # Hier kannst du die Logik für Spielaktionen, Netzwerkaktualisierungen, etc. einfügen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        self.network.send("disconnect")

                # Debug: Zeichne das Fenster schwarz (deine Spiel-Update-Logik gehört hierhin)
                self.win.fill((0, 0, 0))
                pygame.display.update()

            except Exception as e:
                print(f"Fehler in der Spielschleife: {e}")
                self.network.send("disconnect")
                break

        pygame.quit()