import pygame
import os
from network import Network
from player import Player
import json
from ball import Ball





class Client:
    def __init__(self, host = "127.0.0.1"):
        pygame.init()
        pygame.mixer.init()  # Initialisiert den Soundmixer
        pygame.display.init()
        pygame.joystick.init()

        shop_data = json.load(open("Game/MK5/shop_data.json"))
        selected = shop_data["selected_background"]

        self.player_index = 0

        self.hintergrundbild = pygame.image.load(f"Game/MK5/images/background_0{selected}.png").convert()


        songs = [
            "Game/MK5/sounds/bg_music_rick.mp3",
            "Game/MK5/sounds/bg_music_crab_rave.mp3",
            "Game/MK5/sounds/bg_music_fast_pace.mp3"
        ]

        shop_data = json.load(open("Game/MK5/shop_data.json"))
        musik_volume = shop_data.get("music_volume", 0.5)
        selected_song = shop_data.get("selected_song", 0)
        soundfx = shop_data.get("soundfx_on", True)

        if 0 <= selected_song < len(songs):
            song_path = songs[selected_song]
        else:
            song_path = songs[0]

        self.bg_music = pygame.mixer.Sound(song_path)
        self.bg_music.set_volume(musik_volume)

        """aaa"""
        if soundfx:
            self.bg_music.play(-1)

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
        b = Ball(self.win_width - ball.x - ball.radius, ball.y, ball.radius)
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

    def calculate_xp(self, score_winner, score_loser):
        max_score = score_winner
        max_xp = 100


        diff = score_winner - score_loser
        if diff <= 0:
            return 0, 0  # Ungültiges Ergebnis, keine XP

        winner_xp = (diff / max_score) * max_xp
        loser_xp = winner_xp / 2

        return round(winner_xp), round(loser_xp)

    def save_xp(self, winner_xp, loser_xp):
        # shop_data laden
        path = "Game/MK5/shop_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                shop_data = json.load(f)
        else:
            shop_data = {}

        # Bestimmen, ob eigener Spieler Gewinner oder Verlierer ist
        # self.player_index ist 0 oder 1
        # scores enthält z.B. [7, 2] — Index = Spieler
        winner_index = 0 if self.scores[0] > self.scores[1] else 1

        if self.player_index == winner_index:
            # Eigener Spieler hat gewonnen
            current_xp = shop_data.get("xp", 0)
            shop_data["xp"] = current_xp + winner_xp
        else:
            # Eigener Spieler hat verloren
            current_xp = shop_data.get("xp", 0)
            shop_data["xp"] = current_xp + loser_xp

        # zurück in Datei schreiben
        with open(path, "w") as f:
            json.dump(shop_data, f, indent=4)

    def game_loop(self):
        clock = pygame.time.Clock()
        controller = None
        if pygame.joystick.get_count() > 0:
            controller = pygame.joystick.Joystick(0)
            controller.init()

        button_rect = pygame.Rect(self.win_width - 210, 20, 180, 50)
        font_button = pygame.font.SysFont("comicsans", 32)

        while self.run:
            clock.tick(60)
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        self.network.send("disconnect")
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if button_rect.collidepoint(mouse_pos):
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
                    self.player_index = player_index
                    me = players[player_index]
                    enemy = players[1 - player_index]
                    self.ball = ball
                    self.scores = scores

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

                #Exit Button zeichnen
                pygame.draw.rect(self.win, (200, 55, 55), button_rect, border_radius=8)
                text = font_button.render("Spiel beenden", True, (255, 255, 255))
                text_rect = text.get_rect(center=button_rect.center)
                self.win.blit(text, text_rect)

                pygame.display.update()

                if game_over:
                    winner_score = max(self.scores)
                    loser_score = min(self.scores)

                    winner_xp, loser_xp = self.calculate_xp(winner_score, loser_score)
                    print(f"Gewinner XP: {winner_xp}, Verlierer XP: {loser_xp}")

                    self.save_xp(winner_xp, loser_xp)

                    font_big = pygame.font.SysFont("comicsans", 100)
                    text = font_big.render(str(game_over), 1, (255, 0, 0))
                    self.win.blit(text, (self.win_width // 2 - text.get_width() // 2,
                                         self.win_height // 2 - text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.delay(4000)
                    self.run = False

            except Exception as e:
                print(f"Fehler in der Spielschleife: {e}")
                self.run = False
                self.network.send("disconnect")

        import start
        start.main_menu()
        pygame.quit()
        print("Spiel beendet.")