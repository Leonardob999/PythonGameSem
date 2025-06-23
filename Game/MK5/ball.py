import pygame
import random

class Ball:
    def __init__(self, x, y, radius, color=(255, 255, 255), max_speed=9, base_speed=7):
        # Initialisierung der Ball-Attribute:
        # Position (x, y), Radius, Farbe, max Speed, Basisspeed
        self.vel_y = None   # vertikale Geschwindigkeit, wird später gesetzt
        self.vel_x = None   # horizontale Geschwindigkeit, wird später gesetzt
        self.x = x
        self.y = y
        self.start_x = x    # Startposition speichern, um reset zu ermöglichen
        self.start_y = y
        self.radius = radius
        self.color = color
        self.max_speed = max_speed
        self.base_speed = base_speed
        self.reset_position()  # Ballposition und Geschwindigkeit initial setzen

    def reset_position(self):
        # Position auf Startposition zurücksetzen
        self.x = self.start_x
        self.y = self.start_y
        # Zufälliger Winkel für den vertikalen Geschwindigkeitsanteil (-0.5 bis 0.5)
        angle = random.uniform(-0.5, 0.5)
        # horizontale Geschwindigkeit auf Basisspeed, Richtung zufällig links oder rechts
        self.vel_x = self.base_speed * (1 if random.choice([True, False]) else -1)
        # vertikale Geschwindigkeit proportional zum Winkel (int gerundet)
        self.vel_y = int(self.base_speed * angle)

    def draw(self, win):
        # Zeichnet den Ball als Kreis auf das Fenster 'win'
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def intersects(self, player):
        # Prüft, ob der Ball mit einem Player-Objekt kollidiert
        # player.x, player.y, player.width, player.height: Rechteck des Spielers
        circle_distance_x = abs(self.x - (player.x + player.width/2))
        circle_distance_y = abs(self.y - (player.y + player.height/2))

        # Wenn der Abstand größer als die Summe aus halber Breite/Höhe + Radius ist -> keine Kollision
        if circle_distance_x > (player.width/2 + self.radius):
            return False
        if circle_distance_y > (player.height/2 + self.radius):
            return False

        # Ball überlappt horizontal oder vertikal mit dem Spieler -> Kollision
        if circle_distance_x <= (player.width/2):
            return True
        if circle_distance_y <= (player.height/2):
            return True

        # Überprüft die Distanz zum nächsten Eckpunkt (für Kreis-Rechteck-Kollision)
        corner_distance_sq = (circle_distance_x - player.width/2) ** 2 + \
                             (circle_distance_y - player.height/2) ** 2

        # Wenn Abstand zum Eckpunkt kleiner als Radius -> Kollision
        return corner_distance_sq <= (self.radius ** 2)

    def move(self, player1, player2):
        # Bewegt den Ball basierend auf seiner Geschwindigkeit
        self.x += self.vel_x
        self.y += self.vel_y

        # Überprüfung obere Bildschirmkante (y=0)
        if self.y - self.radius <= 0:  # Wenn Ball oben rausgeht
            self.y = self.radius        # Ball bleibt am Rand
            self.vel_y *= -1           # vertikale Richtung umkehren (abprallen)

        # Überprüfung untere Bildschirmkante (hier 800 als Höhe festgelegt)
        elif self.y + self.radius >= 800:
            self.y = 800 - self.radius
            self.vel_y *= -1

        # Links raus (x=0) -> Punkt für Spieler 2
        if self.x - self.radius <= 0:
            return 2  # Spieler 2 bekommt Punkt

        # Rechts raus (x=1000) -> Punkt für Spieler 1
        elif self.x + self.radius >= 1000:
            return 1  # Spieler 1 bekommt Punkt

        # Kollision mit Player1 (links), nur wenn Ball sich nach links bewegt
        if self.intersects(player1) and self.vel_x < 0:
            # Position Ball direkt neben Player1 setzen
            self.x = player1.x + player1.width + self.radius
            # Ermittlung der Aufprallposition auf dem Paddle (zwischen 0 und 1)
            impact_pos = (self.y - player1.y) / player1.height
            # Offset so, dass mittig 0 ist und oben/unten max Geschwindigkeit gibt
            impact_offset = (impact_pos - 0.5) * 2
            # vertikale Geschwindigkeit anpassen proportional zur Position
            self.vel_y = impact_offset * self.max_speed
            # horizontale Geschwindigkeit wird positiv (nach rechts)
            self.vel_x = abs(self.vel_x)

        # Kollision mit Player2 (rechts), nur wenn Ball sich nach rechts bewegt
        elif self.intersects(player2) and self.vel_x > 0:
            self.x = player2.x - self.radius
            impact_pos = (self.y - player2.y) / player2.height
            impact_offset = (impact_pos - 0.5) * 2
            self.vel_y = impact_offset * self.max_speed
            self.vel_x = -abs(self.vel_x)  # Ball bewegt sich nach links

        return 0  # Wenn kein Punkt erzielt wurde, 0 zurückgeben


    def bounced_off_wall(self):
        return self.y - self.radius <= 0 or self.y + self.radius >= 800
