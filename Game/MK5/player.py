import pygame

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
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, controller=None):
        keys = pygame.key.get_pressed()
        joystick_y = 0

        # Überprüfung, ob ein Controller vorhanden ist
        if controller:
            joystick_y = controller.get_axis(1)  # Y-Achse abrufen

        # Tastatursteuerung
        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        # Controller-Steuerung
        if controller:
            if joystick_y < -0.1:  # Stick nach oben
                self.y -= self.vel
            elif joystick_y > 0.1:  # Stick nach unten
                self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
