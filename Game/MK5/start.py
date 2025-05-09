import pygame
import os
import subprocess

# Fenstergröße festlegen
WIN_WIDTH, WIN_HEIGHT = 500, 300
dirname = os.path.dirname(__file__)
client_path = os.path.join(dirname, 'client.py')
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong Start Page")


def start_game():
    pygame.quit()
    subprocess.Popen(["python3", client_path])  # Startet 'client.py' als neuen Prozess



def main():
    run = True
    clock = pygame.time.Clock()

    # Farben definieren
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Schriftart für Button-Text
    font = pygame.font.SysFont("comicsans", 50)

    # Button-Position und Größe
    button_color = white
    button_hover_color = (200, 200, 200)
    button_rect = pygame.Rect(WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 50, 200, 100)

    while run:
        clock.tick(30)
        win.fill(black)  # Hintergrundfarbe

        # Mausposition
        mouse_pos = pygame.mouse.get_pos()

        # Zeichne den Button
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, button_hover_color, button_rect)
        else:
            pygame.draw.rect(win, button_color, button_rect)

        # Button-Text
        text = font.render("Start", True, black)
        win.blit(text, (button_rect.x + button_rect.width // 2 - text.get_width() // 2,
                        button_rect.y + button_rect.height // 2 - text.get_height() // 2))

        pygame.display.update()

        # Ereignisse verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos):
                    start_game()  # Starte das Spiel

    pygame.quit()


if __name__ == "__main__":
    main()