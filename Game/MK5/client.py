import pygame
from network import Network
from player import Player

class GameClient:
    def __init__(self, mode):
        pygame.init()
        pygame.joystick.init()

        self.mode = {"name": mode} if isinstance(mode, str) else mode
        self.win_width = 1000
        self.win_height = 800
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Pong")

        self.player = Player(0, 425, 25, 150, (255, 255, 255))
        self.network = Network()
        self.run = True
        self.scores = [0, 0]
        self.ball = None

    def start(self):
        try:
            # Sende Modus-Info an den Server (Spielstart/Namensauswahl)
            response = self.network.send(self.mode)
            if isinstance(response, tuple) and response[0] == "mode_set":
                self.game_loop()
            else:
                print("Es gab ein Problem beim Setzen des Spielmodus. Antwort:", response)
                return
        except Exception as e:
            print(f"Fehler beim Starten des Spiels: {e}")

    def game_loop(self):
        clock = pygame.time.Clock()
        controller = None
        if pygame.joystick.get_count() > 0:
            controller = pygame.joystick.Joystick(0)
            controller.init()

        while self.run:
            clock.tick(60)
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        self.network.send("disconnect")

                # Spielersteuerung bewegen (Tastatur ODER Controller)
                self.player.move(controller)
                # Begrenzung Spielfeld (zusätzlich zum Player.move)
                if self.player.y < 0:
                    self.player.y = 0
                elif self.player.y > self.win_height - self.player.height:
                    self.player.y = self.win_height - self.player.height

                # Position/Status an den Server schicken:
                data = self.network.send({"y": self.player.y})

                if data is None:
                    print("Keine Daten vom Server erhalten. Beende Spielschleife.")
                    self.run = False
                    break

                if isinstance(data, tuple) and len(data) == 4:
                    other_player, self.ball, self.scores, game_over = data
                else:
                    print("Ungültige Daten vom Server erhalten.")
                    continue

                # Zeichnen
                self.win.fill((0, 0, 0))
                self.player.draw(self.win)
                if other_player:
                    other_player.draw(self.win)
                if self.ball:
                    self.ball.draw(self.win)

                font = pygame.font.SysFont("comicsans", 36)
                score_text = font.render(
                    f"Player 1: {self.scores[0]}   Player 2: {self.scores[1]}", True, (255, 255, 255)
                )
                self.win.blit(score_text, (self.win_width // 2 - score_text.get_width() // 2, 40))

                pygame.display.update()

                if game_over:
                    font_big = pygame.font.SysFont("comicsans", 100)
                    text = font_big.render(str(game_over), 1, (255, 0, 0))
                    self.win.blit(text, (self.win_width // 2 - text.get_width() // 2, self.win_height // 2 - text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.delay(4000)
                    self.run = False

            except Exception as e:
                print(f"Fehler in der Spielschleife: {e}")
                self.run = False
                self.network.send("disconnect")

        pygame.quit()
        print("Spiel beendet.")
