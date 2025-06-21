import pygame
from network import Network
from player import Player
import json

shop_data = json.load(open("Game/MK5/shop_data.json"))
selected = shop_data["selected_background"]



class Client:
    def __init__(self, host = "127.0.0.1"):
        pygame.init()
        pygame.mixer.init()  # Initialisiert den Soundmixer
        pygame.display.init()
        pygame.joystick.init()

        self.hintergrundbild = pygame.image.load(f"Game/MK5/images/background_0{selected + 1}.png").convert()

        self.bg_music_rick = pygame.mixer.Sound("Game/MK5/sounds/bg_music_rick.mp3")  # Pfad anpassen, falls nötig

        self.bg_music_rick.play() # Spiele hintergrundmusik

        self.host = host

        self.win_width = 1000
        self.win_height = 800
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Pong")

        self.player = Player(0, 425, 25, 150, (255, 255, 255))
        self.network = Network(self.host)
        self.run = True
        self.scores = [0, 0]
        self.ball = None
        self.player_index = 0  # Eigener Index: 0=links, 1=rechts


    def invert_y(self, y):
        return y  # Y achse bleibt gleich (oben/unten nicht spiegeln)

    def invert_ball(self, ball):
        from ball import Ball
        b = Ball(self.win_width - ball.x, ball.y, ball.radius)
        b.vel_x = -ball.vel_x
        b.vel_y = ball.vel_y
        return b

    def invert_player(self, player):
        from player import Player
        return Player(self.win_width - player.x - player.width, player.y, player.width, player.height, player.color)

    def invert_scores(self, scores):
        return [scores[1], scores[0]]

    def start(self):
        try:
            # Verbindung zum Server aufbauen und Index erhalten
            reply = self.network.send("ready")
            self.network.send("ready")
            if isinstance(reply, int):
                self.player_index = reply
            else:
                self.player_index = 0
            self.game_loop()
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

                if isinstance(data, tuple) and len(data) == 5:
                    players, player_index, ball, scores, game_over = data

                    me = players[player_index]
                    enemy = players[1 - player_index]

                    if self.player_index == 0:
                        me.x = 0
                        enemy.x = self.win_width - enemy.width
                    else:
                        me.x = self.win_width - me.width  # Spieler 2 bekommt die rechte Seite
                        enemy.x = 0


                        # Ball und Scores zuweisen
                    self.ball = ball

                else:
                    print("Ungültige Daten vom Server erhalten.")
                    continue

                # Zeichnen
                self.win.blit(self.hintergrundbild, (0, 0))
                me.draw(self.win)
                enemy.draw(self.win)
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