import os
import pygame
import sys
import webbrowser
from start import *
import json


pygame.init()


def get_path(rel_path):
    """Gibt den korrekten Pfad zurück – egal ob im PyInstaller-Build oder nicht"""
    if getattr(sys, 'frozen', False):
        # PyInstaller-Pfad
        base_path = sys._MEIPASS
    else:
        # Entwicklungsumgebung
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

# Fenstergröße und Anzeige konfigurieren
WIN_WIDTH, WIN_HEIGHT = 1000, 800
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Shop")  # Fenster-Titel

# Schriften definieren
font = pygame.font.SysFont("arial", 28)
desc_font = pygame.font.SysFont("arial", 20)

# Speicherpfad
SAVE_FILE = "Game/MK5/shop_data.json"

# Hintergrund-Daten
backgrounds = [
    {"id": 0, "name": "Standard", "thumb": get_path("Game/MK5/images/background_00_thumb.png")},  # Kostenlos
    {"id": 1, "name": "colors 1", "thumb": get_path("Game/MK5/images/background_01_thumb.png")},
    {"id": 2, "name": "colors 2", "thumb": get_path("Game/MK5/images/background_02_thumb.png")},
    {"id": 3, "name": "colors 3", "thumb": get_path("Game/MK5/images/background_03_thumb.png")},
    {"id": 4, "name": "psychose", "thumb": get_path("Game/MK5/images/background_04_thumb.png")},
    {"id": 5, "name": "rainbow", "thumb": get_path("Game/MK5/images/background_05_thumb.png")},
]


# Lied-Daten (ohne Bilder)
songs = [
    {"id": 0, "name": "Rick"},
    {"id": 1, "name": "Crab"},
    {"id": 2, "name": "Fast"},
]

# JSON-Daten laden oder Standardwerte
def lade_shop_daten():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Standardwerte setzen
    data.setdefault("owned_backgrounds", [])
    if 0 not in data["owned_backgrounds"]:  # Hintergrund 0 = Standard
        data["owned_backgrounds"].insert(0, 0)

    data.setdefault("owned_songs", [0])
    data.setdefault("selected_song", 0)
    data.setdefault("music_volume", 0.5)
    data.setdefault("soundfx_on", True)

    # selected_background nur setzen, wenn gültig
    if "selected_background" not in data or data["selected_background"] not in data["owned_backgrounds"]:
        data["selected_background"] = data["owned_backgrounds"][0]  # = 0

    return data


# JSON-Daten speichern
def speichere_shop_daten(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# Shop-Hauptmenü
def shop_menu():
    shop_data = lade_shop_daten()
    owned_bgs = shop_data.get("owned_backgrounds", [])
    owned_songs = shop_data.get("owned_songs", [])
    xp = shop_data.get("xp", 0)

    run = True
    while run:
        win.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # --- Hintergrundkaufbereich ---
        thumb_size = (180, 100)
        spacing = 40
        columns = 3  # Maximal 3 Hintergründe pro Zeile
        start_x = WIN_WIDTH // 2 - (columns * (thumb_size[0] + spacing) - spacing) // 2
        start_y = 160
        thumb_rects = []

        for i, bg in enumerate(backgrounds):
            col = i % columns
            row = i // columns
            x = start_x + col * (thumb_size[0] + spacing)
            y = start_y + row * (thumb_size[1] + 60)  # 60 = zusätzlicher vertikaler Abstand

            rect = pygame.Rect(x, y, *thumb_size)
            color = (150, 150, 200) if rect.collidepoint(mouse_pos) else (100, 100, 160)
            pygame.draw.rect(win, color, rect)

            img = pygame.image.load(bg["thumb"])
            img = pygame.transform.scale(img, (thumb_size[0] - 10, thumb_size[1] - 30))
            win.blit(img, (x + 5, y + 5))

            name_label = desc_font.render(bg["name"], True, (255, 255, 255))
            win.blit(name_label, (x + (thumb_size[0] - name_label.get_width()) // 2, y + thumb_size[1] - 22))

            if bg["id"] in owned_bgs:
                status_label = desc_font.render("Gekauft", True, (0, 255, 0))
            else:
                status_label = desc_font.render("Kaufen (50 XP)", True, (255, 255, 0))
            win.blit(status_label, (x + 10, y - 24))

            # Für Klick-Erkennung
            thumb_rects.append((bg["id"], rect))

        # --- Liedkaufbereich ---
        song_box_w, song_box_h = 200, 60

        # Anzahl Hintergrund-Zeilen berechnen
        columns = 3
        rows = (len(backgrounds) + columns - 1) // columns  # z.B. 6 Elemente => 2 Zeilen

        # Y-Position je nach Anzahl der Hintergrundzeilen
        start_y = 160
        vertical_spacing = thumb_size[1] + 60
        song_y = start_y + rows * vertical_spacing + 40  # zusätzlicher Abstand

        song_start_x = WIN_WIDTH // 2 - ((len(songs) * (song_box_w + spacing)) - spacing) // 2

        for i, song in enumerate(songs):
            x = song_start_x + i * (song_box_w + spacing)
            rect = pygame.Rect(x, song_y, song_box_w, song_box_h)
            color = (200, 180, 100) if rect.collidepoint(mouse_pos) else (160, 140, 80)
            pygame.draw.rect(win, color, rect, border_radius=10)

            name_label = desc_font.render(song["name"], True, (0, 0, 0))
            win.blit(name_label, (rect.centerx - name_label.get_width() // 2, rect.centery - name_label.get_height() // 2))

            if song["id"] in owned_songs:
                status = desc_font.render("Gekauft", True, (0, 200, 0))
            else:
                status = desc_font.render("Kaufen (75 XP)", True, (255, 255, 0))
            win.blit(status, (rect.x + 10, rect.y - 22))

        # XP-Anzeige
        xp_label = desc_font.render(f"XP: {xp}", True, (255, 255, 255))
        win.blit(xp_label, (10, 10))

        # Zurück-Button
        back_rect = pygame.Rect(WIN_WIDTH // 2 - 80, WIN_HEIGHT - 80, 160, 45)
        pygame.draw.rect(win, (70, 70, 90), back_rect)
        back_label = font.render("Zurück", True, (255, 255, 255))
        win.blit(back_label, (back_rect.x + 30, back_rect.y + 8))

        pygame.display.update()

        # Ereignisbehandlung
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Hintergründe kaufen
                for bg_id, rect in thumb_rects:
                    if rect.collidepoint(event.pos) and bg_id not in owned_bgs:
                        if xp >= 20:
                            owned_bgs.append(bg_id)
                            xp -= 20
                            shop_data["owned_backgrounds"] = owned_bgs
                            shop_data["xp"] = xp
                            speichere_shop_daten(shop_data)
                        else:
                            print("Nicht genug XP für diesen Hintergrund!")

                # Lieder kaufen
                for song in songs:
                    x = song_start_x + song["id"] * (song_box_w + spacing)
                    rect = pygame.Rect(x, song_y, song_box_w, song_box_h)
                    if rect.collidepoint(event.pos) and song["id"] not in owned_songs:
                        if xp >= 25:
                            owned_songs.append(song["id"])
                            xp -= 25
                            shop_data["owned_songs"] = owned_songs
                            shop_data["xp"] = xp
                            speichere_shop_daten(shop_data)
                        else:
                            print("Nicht genug XP für dieses Lied!")

                # Zurück-Button
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

SAVE_FILE = get_path("Game/MK5/shop_data.json")

# Liste aller verfügbaren Songs (Index = ID)
song_paths = [
    get_path("Game/MK5/sounds/bg_music_rick.mp3"),
    get_path("Game/MK5/sounds/bg_music_crab_rave.mp3"),
    get_path("Game/MK5/sounds/bg_music_fast_pace.mp3")
]

thumb_paths = [
    get_path("Game/MK5/images/background_00_thumb.png"),
    get_path("Game/MK5/images/background_01_thumb.png"),
    get_path("Game/MK5/images/background_02_thumb.png"),
    get_path("Game/MK5/images/background_03_thumb.png"),
    get_path("Game/MK5/images/background_04_thumb.png"),
    get_path("Game/MK5/images/background_05_thumb.png")
]
background_thumbs = [pygame.transform.scale(pygame.image.load(p), (100, 60)) for p in thumb_paths]

def lade_shop_daten():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Standardwerte setzen
    data.setdefault("owned_backgrounds", [])
    if 0 not in data["owned_backgrounds"]:  # Hintergrund 0 = Standard
        data["owned_backgrounds"].insert(0, 0)

    data.setdefault("owned_songs", [0])
    data.setdefault("selected_song", 0)
    data.setdefault("music_volume", 0.5)
    data.setdefault("soundfx_on", True)

    # selected_background nur setzen, wenn gültig
    if "selected_background" not in data or data["selected_background"] not in data["owned_backgrounds"]:
        data["selected_background"] = data["owned_backgrounds"][0]  # = 0

    return data



song_names = ["Rick", "Crab", "Fast"]


def speichere_shop_daten(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def einstellungen_menu():

    shop_data = lade_shop_daten()
    soundfx_on = shop_data.get("soundfx_on", True)
    owned_backgrounds = shop_data.get("owned_backgrounds", [])
    selected_bg = shop_data.get("selected_background", 0)

    owned_songs = shop_data.get("owned_songs", [])
    selected_song = shop_data.get("selected_song", 0)

    musik_volume = shop_data.get("music_volume") #vielleicht , 0.5 hinten ran

    # Slider Position
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

        # Zeichne den Schalter
        fx_btn_rect = pygame.Rect(WIN_WIDTH // 2 - 120, 250, 240, 60)
        fx_color = (80, 200, 80) if soundfx_on else (160, 60, 60)
        pygame.draw.rect(win, fx_color, fx_btn_rect)
        fx_label = info_font.render("Musik: AN" if soundfx_on else "Musik: AUS", True, (10, 10, 10))
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

        # Liedauswahl
        song_label = info_font.render("Lied auswählen:", True, (255, 255, 255))
        win.blit(song_label, (WIN_WIDTH // 2 - song_label.get_width() // 2, 470))

        song_box_w, song_box_h = 140, 50
        song_y = 510
        song_margin = 20
        song_rects = []
        song_x = WIN_WIDTH // 2 - ((len(owned_songs) * (song_box_w + song_margin)) // 2)

        for i, song_index in enumerate(owned_songs):
            rect = pygame.Rect(song_x + i * (song_box_w + song_margin), song_y, song_box_w, song_box_h)
            song_rects.append((song_index, rect))
            box_color = (255, 220, 100) if song_index == selected_song else (120, 100, 60)
            pygame.draw.rect(win, box_color, rect, border_radius=8)

            song_name = song_names[song_index]  # Name aus Liste
            text = info_font.render(song_name, True, (0, 0, 0))
            win.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

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

                # Lautstärke
                if slider_x <= mx <= slider_x + slider_w and slider_y - 12 <= my <= slider_y + slider_h + 12:
                    relativ = mx - slider_x
                    musik_volume = min(max(relativ / slider_w, 0), 1)
                    shop_data["music_volume"] = musik_volume
                    speichere_shop_daten(shop_data)

                # Sound-Schalter
                if fx_btn_rect.collidepoint(event.pos):
                    soundfx_on = not soundfx_on
                    shop_data["soundfx_on"] = soundfx_on
                    speichere_shop_daten(shop_data)
                    if pygame.mixer and pygame.mixer.get_init():
                        if soundfx_on:
                            pygame.mixer.unpause()
                            try:
                                pygame.mixer.music.unpause()
                            except:
                                pass
                        else:
                            pygame.mixer.pause()
                            try:
                                pygame.mixer.music.pause()
                            except:
                                pass

                # Zurück
                if back_rect.collidepoint(mx, my):
                    run = False

                # Hintergrundauswahl
                for bg_index, rect in thumb_rects:
                    if rect.collidepoint(mx, my):
                        selected_bg = bg_index
                        shop_data["selected_background"] = selected_bg
                        speichere_shop_daten(shop_data)

                # Liedauswahl
                for song_index, rect in song_rects:
                    if rect.collidepoint(mx, my):
                        selected_song = song_index
                        shop_data["selected_song"] = selected_song
                        speichere_shop_daten(shop_data)
