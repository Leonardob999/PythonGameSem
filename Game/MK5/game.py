import pygame
import sys


def start_game(mode):
    """
    Startet das Spiel in einem bestimmten Modus (z. B. Infinite Mode, Best of 7).
    :param mode: Der Spielmodus, z.B. 'infinite', 'best_of_7', 'gauntlet'
    """

    # Fenstergröße
    WIN_WIDTH, WIN_HEIGHT = 1000, 800

    # Objekteinstellungen
    BALL_RADIUS = 10
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 150

    # Farben
    BG_COLOR = (0, 0, 0)
    PADDLE_COLOR = BALL_COLOR = (255, 255, 255)
    TEXT_COLOR = (255, 255, 255)

    # Geschwindigkeit
    ball_speed_x, ball_speed_y = 5, 5
    paddle_speed = 7

    # Initialpositionen
    ball_x, ball_y = WIN_WIDTH // 2, WIN_HEIGHT // 2
    paddle1_y, paddle2_y = WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2, WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2

    # Punktestände
    score1, score2 = 0, 0
    max_score = 4 if mode == "best_of_7" else float("inf")  # Punktelimit nur für Best of 7

    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(f"Pong - {mode.capitalize()}")

    run = True
    while run:
        win.fill(BG_COLOR)

        # Ereignisse prüfen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Steuerung
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < WIN_HEIGHT - PADDLE_HEIGHT:
            paddle1_y += paddle_speed
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2_y < WIN_HEIGHT - PADDLE_HEIGHT:
            paddle2_y += paddle_speed

        # Ballbewegung
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball Kollision mit der oberen und unteren Wand
        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= WIN_HEIGHT:
            ball_speed_y *= -1

        # Ball Kollision mit den Paddles
        if (ball_x - BALL_RADIUS <= PADDLE_WIDTH and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT):
            ball_speed_x *= -1

        if (ball_x + BALL_RADIUS >= WIN_WIDTH - PADDLE_WIDTH and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT):
            ball_speed_x *= -1

        # Punktevergabe bei Toren
        if ball_x - BALL_RADIUS < 0:  # Spieler 2 punktet
            score2 += 1
            ball_x, ball_y = WIN_WIDTH // 2, WIN_HEIGHT // 2  # Ball zurücksetzen
            ball_speed_x *= -1

        if ball_x + BALL_RADIUS > WIN_WIDTH:  # Spieler 1 punktet
            score1 += 1
            ball_x, ball_y = WIN_WIDTH // 2, WIN_HEIGHT // 2  # Ball zurücksetzen
            ball_speed_x *= -1

        # Siegbedingungen für 'Best of 7'
        if mode == "best_of_7":
            if score1 == max_score:
                display_winner(win, "Spieler 1")
                return  # Spiel beendet → zurück ins Menü
            elif score2 == max_score:
                display_winner(win, "Spieler 2")
                return  # Spiel beendet → zurück ins Menü

        # Ball und Paddles zeichnen
        pygame.draw.rect(win, PADDLE_COLOR, (0, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(win, PADDLE_COLOR, (WIN_WIDTH - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(win, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

        # Punktestände anzeigen
        font = pygame.font.SysFont("comicsans", 50)
        score_text = font.render(f"{score1} : {score2}", True, TEXT_COLOR)
        win.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)


def display_winner(win, winner):
    """
    Zeigt den Gewinner-Bildschirm an.
    :param win: Das Pygame-Fenster.
    :param winner: Gewinner-Spieler (als String).
    """
    run = True
    while run:
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("comicsans", 60)
        winner_text = font.render(f"{winner} hat gewonnen!", True, (255, 255, 255))
        win.blit(winner_text, (
        win.get_width() // 2 - winner_text.get_width() // 2, win.get_height() // 2 - winner_text.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
