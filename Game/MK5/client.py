import pygame
from network import Network
from player import Player
from ball import Ball

width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, player, player2, ball):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    ball.draw()
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getP()
    b = n.getB
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2, b)

main()