import pygame  # Stelle sicher, dass pygame importiert ist


class Ball():
    def __init__(self, x, y, radius, vel_x=3, vel_y=3):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel_x = vel_x  # Ballgeschwindigkeit in X-Richtung
        self.vel_y = vel_y  # Ballgeschwindigkeit in Y-Richtung
        self.initial_x = x  # Ursprüngliche X-Position (für Reset)
        self.initial_y = y  # Ursprüngliche Y-Position (für Reset)


    def reset_position(self):
        # Setze den Ball in die Mitte zurück
        self.x = self.initial_x
        self.y = self.initial_y
        self.vel_x *= -1  # Richtung umkehren, um Abwechslung zu schaffen

    def move(self, player1, player2):
        # Ballbewegung
        self.x += self.vel_x
        self.y += self.vel_y

        # Kollision mit dem oberen und unteren Spielfeldrand
        if self.y - self.radius <= 0 or self.y + self.radius >= 1000:
            self.vel_y *= -1

        # Prüfen, ob der Ball ein Tor erzielt hat
        if self.x - self.radius <= 0:  # Linkes Tor
            return 2  # Spieler 2 bekommt einen Punkt
        elif self.x + self.radius >= 1000:  # Rechtes Tor
            return 1  # Spieler 1 bekommt einen Punkt

        # Kollision mit den Spielern (Schlägern)
        if self.collide(player1) or self.collide(player2):
            self.vel_x *= -1

        return 0  # Kein Punkt erzielt

    def collide(self, player):
        # Prüfen, ob der Ball mit einem Spieler kollidiert
        if (self.x - self.radius <= player.x + player.width and self.x + self.radius >= player.x):
            if self.y + self.radius >= player.y and self.y - self.radius <= player.y + player.height:
                return True
        return False

    def draw(self, win):
        # Ball auf dem Spielfeld zeichnen
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.radius)
