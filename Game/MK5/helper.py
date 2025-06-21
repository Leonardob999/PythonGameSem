import os
import pygame
import sys
import webbrowser
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
    desc_font = pygame.font.SysFont("arial", 22)
    coin_font = pygame.font.SysFont("arial", 28)

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
            pygame.draw.rect(win, color, rect)

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
            pygame.draw.rect(win, color, rect)

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

        """Zurück-Button
                   back_rect = draw_button(win, "Zurück", WIN_WIDTH // 2 - 160, WIN_HEIGHT - 60, 320, 50)
                   back_rect = draw_button(win, "Zurück", WIN_WIDTH // 2 - 160, 700, 350, 80)


                   # Mauspositionen für Hover-Effekte
                   mouse_pos = pygame.mouse.get_pos()
                   draw_button(win, "Zurück", WIN_WIDTH // 2 - 160, 700, 350, 80,
                               back_rect.collidepoint(mouse_pos))"""

        info_font = pygame.font.SysFont("arial", 22)

        # Zurück-Button
        back_rect = pygame.Rect(WIN_WIDTH // 2 - 80, WIN_HEIGHT - 80, 160, 45)
        pygame.draw.rect(win, (70, 70, 90), back_rect)
        back_label = info_font.render("Zurück", True, (255, 255, 255))
        win.blit(back_label, (back_rect.x + 35, back_rect.y + 8))




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
                        open_link_window()
                for rect, item in powerup_buttons:
                    if rect.collidepoint(event.pos):
                        print(f"Powerup {item['name']} ausgewählt!")
                        # Hier Powerup-Kauf-Logik

                if back_rect.collidepoint(event.pos):
                    run = False



def open_link_window():
    pygame.init()
    W, H = 320, 120
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Mehr Infos")
    font = pygame.font.SysFont('arial', 30, bold=True)

    link_rect = pygame.Rect(60, 40, 200, 40)
    link_color = (100, 100, 255)
    text_color = (255, 255, 255)
    bg_color = (240, 240, 240)

    running = True
    while running:
        screen.fill(bg_color)
        pygame.draw.rect(screen, link_color, link_rect, border_radius=7)
        text = font.render("Moneten Moneten", True, text_color)
        screen.blit(text, (link_rect.left + 12, link_rect.top + 5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if link_rect.collidepoint(event.pos):
                    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    running = False  # Fenster schließen nach Klick

    pygame.quit()

# So kannst du das Fenster aufrufen:
if __name__ == "__main__":
    open_link_window()






def einstellungen_menu():
    # Globale Variablen um Einstellungen zu merken
    global soundfx_on, musik_volume

    # Initialwerte, falls nicht gesetzt
    try:
        soundfx_on
    except NameError:
        soundfx_on = True
    try:
        musik_volume
    except NameError:
        musik_volume = 0.5

    run = True
    font = pygame.font.SysFont("arial", 32)
    info_font = pygame.font.SysFont("arial", 22)

    # Schieberegler für Musiklautstärke
    slider_x = WIN_WIDTH // 2 - 160
    slider_y = 160
    slider_w = 3200
    slider_h = 12

    while run:
        win.fill((0,0,0))
        pygame.mixer.init()
        self.collision_sound.set_volume(musik_volume) # Lautstärke einstellen (Wert zwischen 0.0 und 1.0)

        # Überschrift
        label = font.render("Einstellungen", True, (255,255,255))
        win.blit(label, (WIN_WIDTH//2-label.get_width()//2, 60))

        # --- Musiklautstärke-Schieberegler anzeigen ---
        vol_label = info_font.render(f"Musiklautstärke: {int(musik_volume*100)}%", True, (200,200,200))
        win.blit(vol_label, (slider_x, slider_y-36))

        # Slider-Balken
        pygame.draw.rect(win, (100,100,105), (slider_x, slider_y, slider_w, slider_h), border_radius=5)
        # Slider 'Knopf'
        knob_x = int(slider_x + musik_volume*slider_w)
        pygame.draw.circle(win, (200,170,80), (knob_x, slider_y+slider_h//2), 16)

        # --- Soundeffekt-Button anzeigen ---
        fx_btn_rect = pygame.Rect(WIN_WIDTH//2 - 120, 250, 240, 60)
        fx_color = (80,200,80) if soundfx_on else (160,60,60)
        pygame.draw.rect(win, fx_color, fx_btn_rect)
        fx_label = info_font.render("Soundeffekte: AN" if soundfx_on else "Soundeffekte: AUS", True, (10,10,10))
        win.blit(fx_label, (fx_btn_rect.x + 24, fx_btn_rect.y + fx_btn_rect.height//2 - fx_label.get_height()//2))

        # Zurück-Button
        back_rect = pygame.Rect(WIN_WIDTH//2-80, WIN_HEIGHT-80, 160, 45)
        pygame.draw.rect(win, (70,70,90), back_rect)
        back_label = info_font.render("Zurück", True, (255,255,255))
        win.blit(back_label, (back_rect.x+35, back_rect.y+8))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Schieberegler?
                if (slider_x <= mx <= slider_x+slider_w) and (slider_y-12 <= my <= slider_y+slider_h+12):
                    relativ = mx - slider_x
                    musik_volume = min(max(relativ/slider_w, 0), 1)
                    pygame.mixer.music.set_volume(musik_volume)
                # Soundeffekt-Schalter?
                if fx_btn_rect.collidepoint(mx,my):
                    soundfx_on = not soundfx_on
                # Zurück?
                if back_rect.collidepoint(mx,my):
                    run = False

        # Ziehen auf Schieberegler
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if (slider_x <= mx <= slider_x+slider_w) and (slider_y-12 <= my <= slider_y+slider_h+12):
                relativ = mx - slider_x
                musik_volume = min(max(relativ/slider_w, 0), 1)
                pygame.mixer.music.set_volume(musik_volume)