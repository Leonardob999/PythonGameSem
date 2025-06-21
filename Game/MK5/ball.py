import pygame
import random

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.radius = radius
        self.color = (255, 255, 255)
        self.max_speed = 9
        self.base_speed = 7
        self.reset_position()

        # Lade den Sound für die Kollision
        self.collision_sound = pygame.mixer.Sound("Game/MK5/sounds/bounce.wav")  # Pfad anpassen!


    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        angle = random.uniform(-0.5, 0.5)
        self.vel_x = self.base_speed * (1 if random.choice([True, False]) else -1)
        self.vel_y = int(self.base_speed * angle)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def intersects(self, player):
        circle_distance_x = abs(self.x - (player.x + player.width/2))
        circle_distance_y = abs(self.y - (player.y + player.height/2))

        if circle_distance_x > (player.width/2 + self.radius):
            return False
        if circle_distance_y > (player.height/2 + self.radius):
            return False

        if circle_distance_x <= (player.width/2):
            return True
        if circle_distance_y <= (player.height/2):
            return True

        corner_distance_sq = (circle_distance_x - player.width/2) ** 2 + \
                             (circle_distance_y - player.height/2) ** 2

        return corner_distance_sq <= (self.radius ** 2)

    def move(self, player1, player2):
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vel_y *= -1
        elif self.y + self.radius >= 800:
            self.y = 800 - self.radius
            self.vel_y *= -1

        if self.x - self.radius <= 0:
            return 2
        elif self.x + self.radius >= 1000:
            return 1

        if self.intersects(player1) and self.vel_x < 0:
            # Spiele Kollision-Sound
            self.collision_sound.play()

            self.x = player1.x + player1.width + self.radius
            impact_pos = (self.y - player1.y) / player1.height
            impact_offset = (impact_pos - 0.5) * 2
            self.vel_y = impact_offset * self.max_speed
            self.vel_x = abs(self.vel_x)

        elif self.intersects(player2) and self.vel_x > 0:
            # Spiele Kollision-Sound
            self.collision_sound.play()

            self.x = player2.x - self.radius
            impact_pos = (self.y - player2.y) / player2.height
            impact_offset = (impact_pos - 0.5) * 2
            self.vel_y = impact_offset * self.max_speed
            self.vel_x = -abs(self.vel_x)

        """self.collision_sound.set_volume(0.5)  # Lautstärke einstellen (Wert zwischen 0.0 und 1.0)"""

        return 0