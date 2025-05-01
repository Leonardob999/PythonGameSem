import pygame

class Ball():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.circle = (x, y, radius)
        self.vel = 3

    def draw(self, win):
        pygame.draw.circle(win,(255,255,255) , self.circle)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.x -= self.vel

        if keys[pygame.K_LEFT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.circle = (self.x, self.y, self.radius)
