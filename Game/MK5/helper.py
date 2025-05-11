import os
from start import *

def shop_menu():
    """Shop-Menü mit Powerups unten und Coin-Angeboten nebeneinander oben."""

    # Powerup-Items (weiterhin untereinander, aber kleiner & weiter unten)

    dirname = os.path.dirname(__file__)

    shop_items = [
        {"name": "Power-Up", "text": "Erhöht deine Geschwindigkeit!", "image": os.path.join(dirname, 'images/powerup.png')},
        {"name": "Extra-Leben", "text": "Du bekommst ein weiteres Leben.", "image": os.path.join(dirname, 'images/leben.png')},
        {"name": "Schutzschild", "text": "Schützt dich vor Angriffen.", "image": os.path.join(dirname, 'images/schild.png')},
    ]

    # Coin-Angebote (kleine Felder, nebeneinander)
    shop_coins = [
        {"name": "100", "text": "Armer schlucker", "image": os.path.join(dirname, 'images/100.png')},
        {"name": "500", "text": "Aight", "image": os.path.join(dirname, 'images/500.png')},
        {"name": "1000", "text": "Geil", "image": os.path.join(dirname, 'images/1000.png')},
    ]

    # Layout: kleinere Felder
    powerup_button_height = 70
    powerup_button_width = 400
    powerup_spacing = 18
    base_powerup_x = WIN_WIDTH // 2 - powerup_button_width // 2
    # weiter unten platzieren:
    base_powerup_y = WIN_HEIGHT - (len(shop_items) * (powerup_button_height + powerup_spacing)) - 100

    # Coins: noch kleinere Felder, nebeneinander oben
    coin_box_size = 150
    coin_spacing = 30
    base_coin_y = 80
    # Coins nebeneinander mittig angeordnet
    total_coins_width = len(shop_coins) * coin_box_size + (len(shop_coins) - 1) * coin_spacing
    start_coin_x = WIN_WIDTH // 2 - total_coins_width // 2

    # Schriftarten
    desc_font = pygame.font.SysFont("comicsans", 22)
    coin_font = pygame.font.SysFont("comicsans", 28)

    run = True
    while run:
        win.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        powerup_buttons = []
        coin_buttons = []

        # Coin-Angebote anzeigen (nebeneinander)
        for idx, coin in enumerate(shop_coins):
            x = start_coin_x + idx * (coin_box_size + coin_spacing)
            y = base_coin_y
            rect = pygame.Rect(x, y, coin_box_size, coin_box_size)
            color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(win, color, rect, border_radius=10)

            # Bild für Coin
            try:
                img = pygame.image.load(coin["image"])
                img = pygame.transform.scale(img, (coin_box_size - 26, coin_box_size - 38))
                win.blit(img, (x + 13, y + 8))
            except Exception as e:
                print(f"Fehler beim Laden von {coin['image']}: {e}")




            name_label = coin_font.render(coin["name"], True, BLACK)
            name_x = x + (coin_box_size - name_label.get_width()) // 2
            win.blit(name_label, (name_x, y + coin_box_size - 37))
            text_label = desc_font.render(coin["text"], True, BLACK)
            text_x = x + (coin_box_size - text_label.get_width()) // 2
            win.blit(text_label, (text_x, y + coin_box_size - 17))

            coin_buttons.append((rect, coin))

        # Powerups anzeigen (untereinander, weiter unten)
        for idx, item in enumerate(shop_items):
            y = base_powerup_y + idx * (powerup_button_height + powerup_spacing)
            rect = pygame.Rect(base_powerup_x, y, powerup_button_width, powerup_button_height)
            color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(win, color, rect, border_radius=12)

            # Bild
            try:
                img = pygame.image.load(item["image"])
                img = pygame.transform.scale(img, (powerup_button_height - 14, powerup_button_height - 14))
                win.blit(img, (base_powerup_x + 10, y + 7))
            except Exception as e:
                print(f"Fehler beim Laden von {coin['image']}: {e}")



            # Name & Text
            label = font.render(item["name"], True, BLACK)
            win.blit(label, (base_powerup_x + powerup_button_height, y + 8))
            desc = desc_font.render(item["text"], True, BLACK)
            win.blit(desc, (base_powerup_x + powerup_button_height, y + 38))
            powerup_buttons.append((rect, item))

        # Zurück-Button
        back_rect = draw_button(win, "Zurück", WIN_WIDTH // 2 - 160, WIN_HEIGHT - 60, 320, 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, coin in coin_buttons:
                    if rect.collidepoint(event.pos):
                        print(f"Coin-Pack {coin['name']} ausgewählt!")
                        # Hier Coin-Kauf-Logik
                for rect, item in powerup_buttons:
                    if rect.collidepoint(event.pos):
                        print(f"Powerup {item['name']} ausgewählt!")
                        # Hier Powerup-Kauf-Logik
                if back_rect.collidepoint(event.pos):
                    run = False