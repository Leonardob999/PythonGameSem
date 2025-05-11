import socket
from _thread import start_new_thread
from player import Player
from ball import Ball
import pickle
import time

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print(f"[DEBUG] Server gestartet auf {server}:{port}")
except socket.error as e:
    print(f"[ERROR] Fehler beim Binden: {e}")
    exit(1)

s.listen(2)
print("Waiting for a connection, Server Started")

DEFAULTS = {
    "player_height": 150,
    "player_width": 25,
    "player_color": (255, 255, 255),
    "ball_radius": 15,
    "ball_speed": 10,
    "ball_color": (255, 255, 255),
    "max_score": None
}

# Zuweisungs-Logik für Gamemode: Schlüssel → Lambda(logik)
GAME_MODE_APPLIER = {
    "player_height": lambda value: [setattr(p, "height", value) for p in players],
    "player_width": lambda value: [setattr(p, "width", value) for p in players],
    "player_color": lambda value: [setattr(p, "color", value) for p in players],
    "ball_radius": lambda value: setattr(ball, "radius", value),
    "ball_speed": lambda value: (setattr(ball, "vel_x", value), setattr(ball, "vel_y", value)),
    "ball_color": lambda value: setattr(ball, "color", value),
    "max_score": lambda value: None
}


players = [Player(0, 425, 25, 150, (255, 255, 255)), Player(975, 425, 25, 150, (255, 255, 255))]
ball = Ball(500, 400, 15)  # y auf 400, weil Höhe = 800

scores = [0, 0]
currentPlayer = 0
game_mode = None
player_inputs = [None, None]
max_score = None

def apply_game_mode(game_mode):
    """
    Wendet für alle Werte im game_mode die passende Änderung im Spiel an.
    """
    global players, ball, max_score
    if not game_mode:
        return
    for key, value in game_mode.items():
        if key in GAME_MODE_APPLIER:
            GAME_MODE_APPLIER[key](value)
    # Speichere max_score extra
    max_score = game_mode["max_score"] if "max_score" in game_mode else DEFAULTS["max_score"]

def reset_to_defaults():
    """
    Setzt alle Werte auf die Default-Settings zurück.
    """
    apply_game_mode(DEFAULTS)

def threaded_client(conn, player):
    global ball, scores, players, currentPlayer, game_mode, player_inputs, max_score

    print("[DEBUG] Threaded Client: Start")
    print("[DEBUG] game_mode ist:", game_mode)
    try:
        reset_to_defaults()
        print("[DEBUG] Defaults ok")
        apply_game_mode(game_mode)
        print("[DEBUG] game_mode angewendet")
    except Exception as e:
        print("[ERROR] Initialisierung im Thread fehlgeschlagen:", e)
    conn.sendall(pickle.dumps("connected"))
    print("[DEBUG] Begrüßung versendet")

    try:
        print(f"[DEBUG] Client {player} verbunden. Warte auf Daten...")
        data = conn.recv(8192)
        if not data:
            print(f"[DEBUG] Client {player} hat die Verbindung geschlossen.")
            return
        data = pickle.loads(data)
        if isinstance(data, dict) and "name" in data:
            game_mode = data
            print(f"[DEBUG] Spielmodus vom Spieler 1 gesetzt: {game_mode}")

            # Wende hier den Spielmodus an!
            apply_game_mode(game_mode)

            conn.sendall(pickle.dumps(("mode_set", True)))
        else:
            conn.sendall(pickle.dumps(("invalid_mode", False)))
            return

        # Index senden
        index_sent = False

        while True:
            data = conn.recv(8192)
            if not data:
                print(f"[DEBUG] Client {player} hat die Verbindung geschlossen.")
                break

            # Auf Anfrage Index:
            try:
                loaded = pickle.loads(data)
            except Exception:
                continue

            if loaded == {} and not index_sent:
                conn.sendall(pickle.dumps(player))
                index_sent = True
                continue

            # Spielerbewegungen empfangen
            if isinstance(loaded, dict) and 'y' in loaded:
                player_inputs[player] = loaded

            if any(player_inputs):
                if player_inputs[0] is not None:
                    players[0].y = player_inputs[0]['y']
                if player_inputs[1] is not None:
                    players[1].y = player_inputs[1]['y']
                punkt = ball.move(players[0], players[1])

                if punkt == 1:
                    scores[0] += 1
                    ball.reset_position()
                elif punkt == 2:
                    scores[1] += 1
                    ball.reset_position()

            other_player = players[1] if player == 0 else players[0]
            game_over = False

            # Nur bei gesetztem max_score prüfen, ob jemand gewonnen hat
            if max_score is not None:
                if scores[0] >= max_score:
                    game_over = "Player 1 gewinnt!"
                elif scores[1] >= max_score:
                    game_over = "Player 2 gewinnt!"

            response = pickle.dumps(
                (other_player, ball, scores, game_over)
            )
            conn.sendall(response)
            time.sleep(1 / 60.0)
    except Exception as e:
        print(f"[ERROR] Fehler bei Client {player}: {e}")
    finally:
        conn.close()
        print(f"[DEBUG] Verbindung zu Client {player} geschlossen.")

while True:
    try:
        conn, addr = s.accept()
        print(f"[DEBUG] Verbunden mit: {addr}")
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
    except Exception as e:
        print(f"[ERROR] Fehler beim Akzeptieren einer Verbindung: {e}")
        break

s.close()