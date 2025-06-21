import os
import pygame
import sys
import webbrowser
from start import *
import json
"""
def shop_menu():


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
                    """


pygame.init()

# Fenstergröße und Anzeige konfigurieren
WIN_WIDTH, WIN_HEIGHT = 1000, 800
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Shop")  # Fenster-Titel

# Schriften definieren
font = pygame.font.SysFont("arial", 28)
desc_font = pygame.font.SysFont("arial", 20)

# Pfad zur Speicherdatei für gekaufte und ausgewählte Hintergründe
SAVE_FILE = "Game/MK5/shop_data.json"

# Liste mit verfügbaren Hintergründen im Shop
backgrounds = [
    {"id": 0, "name": "Wald", "thumb": "Game/MK5/images/background_01_thumb.png"},
    {"id": 1, "name": "Wüste", "thumb": "Game/MK5/images/background_02_thumb.png"},
    {"id": 2, "name": "Stadt", "thumb": "Game/MK5/images/background_03_thumb.png"},
]

# Lese vorhandene Shop-Daten aus der JSON-Datei (oder verwende Defaults)
def lade_shop_daten():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"owned_backgrounds": [], "selected_background": 0}

# Speichere aktualisierte Shop-Daten zurück in die JSON-Datei
def speichere_shop_daten(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# Hauptfunktion für das Shop-Menü
def shop_menu():
    shop_data = lade_shop_daten()
    owned = shop_data.get("owned_backgrounds", [])  # Gekaufte Hintergründe

    run = True
    while run:
        win.fill((0, 0, 0))  # Fenster schwarz füllen
        mouse_pos = pygame.mouse.get_pos()  # Aktuelle Mausposition

        # Layout-Einstellungen für die Vorschaubilder
        thumb_size = (180, 100)
        spacing = 40
        total_width = len(backgrounds) * (thumb_size[0] + spacing) - spacing
        start_x = WIN_WIDTH // 2 - total_width // 2
        y = 200  # Y-Position der Thumbnails

        # Zeige alle Hintergrundoptionen
        for i, bg in enumerate(backgrounds):
            x = start_x + i * (thumb_size[0] + spacing)
            rect = pygame.Rect(x, y, *thumb_size)
            # Farbe ändern, wenn Maus drüber ist
            color = (150, 150, 200) if rect.collidepoint(mouse_pos) else (100, 100, 160)
            pygame.draw.rect(win, color, rect)

            # Lade und zeichne das Vorschaubild
            img = pygame.image.load(bg["thumb"])
            img = pygame.transform.scale(img, (thumb_size[0] - 10, thumb_size[1] - 30))
            win.blit(img, (x + 5, y + 5))

            # Zeige Namen des Hintergrunds
            name_label = desc_font.render(bg["name"], True, (255, 255, 255))
            win.blit(name_label, (x + (thumb_size[0] - name_label.get_width()) // 2, y + thumb_size[1] - 22))

            # Zeige Status: "Gekauft" oder "Kaufen"
            if bg["id"] in owned:
                status_label = desc_font.render("Gekauft", True, (0, 255, 0))
            else:
                status_label = desc_font.render("Kaufen", True, (255, 255, 0))
            win.blit(status_label, (x + 10, y - 24))

        # Zeichne "Zurück"-Button unten
        back_rect = pygame.Rect(WIN_WIDTH // 2 - 80, WIN_HEIGHT - 80, 160, 45)
        pygame.draw.rect(win, (70, 70, 90), back_rect)
        back_label = font.render("Zurück", True, (255, 255, 255))
        win.blit(back_label, (back_rect.x + 30, back_rect.y + 8))

        pygame.display.update()  # Aktualisiere den Bildschirm

        # Ereignisbehandlung
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Bei Mausklick prüfen, ob ein Thumbnail oder der Zurück-Button angeklickt wurde
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bg in backgrounds:
                    x = start_x + bg["id"] * (thumb_size[0] + spacing)
                    rect = pygame.Rect(x, y, *thumb_size)
                    if rect.collidepoint(event.pos) and bg["id"] not in owned:
                        # Hintergrund als "gekauft" speichern
                        owned.append(bg["id"])
                        shop_data["owned_backgrounds"] = owned
                        speichere_shop_daten(shop_data)

                # Wenn "Zurück" gedrückt wurde, Menü verlassen
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




pygame.init()
WIN_WIDTH, WIN_HEIGHT = 1000, 800
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Einstellungen")

font = pygame.font.SysFont("arial", 32)
info_font = pygame.font.SysFont("arial", 22)

SAVE_FILE = "Game/MK5/shop_data.json"

thumb_paths = [
    "Game/MK5/images/background_01_thumb.png",
    "Game/MK5/images/background_02_thumb.png",
    "Game/MK5/images/background_03_thumb.png"
]
background_thumbs = [pygame.transform.scale(pygame.image.load(p), (100, 60)) for p in thumb_paths]

def lade_shop_daten():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"owned_backgrounds": [], "selected_background": 0}

def speichere_shop_daten(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def einstellungen_menu():
    shop_data = lade_shop_daten()
    owned_backgrounds = shop_data.get("owned_backgrounds", [])
    selected_bg = shop_data.get("selected_background", 0)
    musik_volume = 0.5
    soundfx_on = True

    slider_x = WIN_WIDTH // 2 - 160
    slider_y = 160
    slider_w = 320
    slider_h = 12

    run = True
    while run:
        win.fill((0, 0, 0))

        label = font.render("Einstellungen", True, (255, 255, 255))
        win.blit(label, (WIN_WIDTH // 2 - label.get_width() // 2, 60))

        # Musiklautstärke
        vol_label = info_font.render(f"Musiklautstärke: {int(musik_volume * 100)}%", True, (200, 200, 200))
        win.blit(vol_label, (slider_x, slider_y - 36))
        pygame.draw.rect(win, (100, 100, 105), (slider_x, slider_y, slider_w, slider_h), border_radius=5)
        knob_x = int(slider_x + musik_volume * slider_w)
        pygame.draw.circle(win, (200, 170, 80), (knob_x, slider_y + slider_h // 2), 16)

        # Soundeffekte
        fx_btn_rect = pygame.Rect(WIN_WIDTH // 2 - 120, 250, 240, 60)
        fx_color = (80, 200, 80) if soundfx_on else (160, 60, 60)
        pygame.draw.rect(win, fx_color, fx_btn_rect)
        fx_label = info_font.render("Soundeffekte: AN" if soundfx_on else "Soundeffekte: AUS", True, (10, 10, 10))
        win.blit(fx_label, (fx_btn_rect.x + 24, fx_btn_rect.y + fx_btn_rect.height // 2 - fx_label.get_height() // 2))

        # Hintergrundauswahl
        inv_label = info_font.render("Hintergrund auswählen:", True, (255, 255, 255))
        win.blit(inv_label, (WIN_WIDTH // 2 - inv_label.get_width() // 2, 340))

        thumb_y = 380
        thumb_margin = 20
        thumb_rects = []
        thumb_x = WIN_WIDTH // 2 - ((len(owned_backgrounds) * (100 + thumb_margin)) // 2)

        for i, bg_index in enumerate(owned_backgrounds):
            thumb = background_thumbs[bg_index]
            rect = pygame.Rect(thumb_x + i * (100 + thumb_margin), thumb_y, 100, 60)
            thumb_rects.append((bg_index, rect))
            win.blit(thumb, (rect.x, rect.y))
            border_color = (255, 255, 0) if bg_index == selected_bg else (100, 100, 100)
            pygame.draw.rect(win, border_color, rect, 3)

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
                mx, my = event.pos

                if slider_x <= mx <= slider_x + slider_w and slider_y - 12 <= my <= slider_y + slider_h + 12:
                    relativ = mx - slider_x
                    musik_volume = min(max(relativ / slider_w, 0), 1)

                if fx_btn_rect.collidepoint(mx, my):
                    soundfx_on = not soundfx_on

                if back_rect.collidepoint(mx, my):
                    run = False

                for bg_index, rect in thumb_rects:
                    if rect.collidepoint(mx, my):
                        selected_bg = bg_index
                        shop_data["selected_background"] = selected_bg
                        speichere_shop_daten(shop_data)