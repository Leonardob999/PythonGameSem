import pygame

WIN_WIDTH, WIN_HEIGHT = 1000, 800

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 6

    def draw(self, win):
        self.update()
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, controller=None):
        keys = pygame.key.get_pressed()
        joystick_y = 0

        # Überprüfung, ob ein Controller vorhanden ist
        if controller:
            joystick_y = controller.get_axis(1)  # Y-Achse abrufen

        # Tastatursteuerung (optional, falls kein Controller verwendet wird)
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        # Controller-Steuerung (absolute Position, basierend auf Stickposition)
        if controller:
            if abs(joystick_y) > 0.1:  # Totezone, um kleinere Bewegungen zu ignorieren
                # Berechne absolute Y-Position basierend auf Controller-Stick
                self.y = (joystick_y + 1) / 2 * (WIN_HEIGHT - self.height)

        # Grenzen der Spielfläche berücksichtigen
        if self.y < 0:
            self.y = 0
        elif self.y > WIN_HEIGHT - self.height:
            self.y = WIN_HEIGHT - self.height

        # Spielerrechteck aktualisieren
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
