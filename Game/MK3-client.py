import pygame
import socket

# Client-Konfiguration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# Spielfeldgrößen
WIDTH = 800
HEIGHT = 600

# Schläger und Ball
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Socket für die Verbindung zum Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Schläger-Positionen
paddle_left = HEIGHT // 2 - 50
paddle_right = HEIGHT // 2 - 50

# Spiel-Schleife
running = True
while running:
    screen.fill((0, 0, 0))  # Hintergrundfarbe

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Eingaben für Schläger (W, S für links, Pfeiltasten für rechts)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_left > 0:
        paddle_left -= 10
    if keys[pygame.K_s] and paddle_left < HEIGHT - PADDLE_HEIGHT:
        paddle_left += 10

    if keys[pygame.K_UP] and paddle_right > 0:
        paddle_right -= 10
    if keys[pygame.K_DOWN] and paddle_right < HEIGHT - PADDLE_HEIGHT:
        paddle_right += 10

    # Position des linken Schlägers an den Server senden
    client_socket.send(str(paddle_left).encode())

    # Empfang von Spielstatus (Ballposition, Schlägerpositionen)
    game_data = client_socket.recv(1024).decode()
    ball_x, ball_y, paddle_left_pos, paddle_right_pos = map(int, game_data.split(','))

    # Ball und Schläger zeichnen
    pygame.draw.rect(screen, (255, 255, 255), (0, paddle_left, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH - PADDLE_WIDTH, paddle_right_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, (255, 255, 255), (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    pygame.display.flip()

pygame.quit()
client_socket.close()
