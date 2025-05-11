import socket
from _thread import start_new_thread
from player import Player
from ball import Ball
import pickle
import time

server = "100.101.29.26"
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

players = [Player(0, 425, 25, 150, (255, 255, 255)), Player(950, 425, 25, 150, (255, 255, 255))]
ball = Ball(500, 400, 15)  # y auf 400, weil Höhe = 800

scores = [0, 0]
currentPlayer = 0
game_mode = None
player_inputs = [None, None]

def threaded_client(conn, player):
    global ball, scores, players, currentPlayer, game_mode, player_inputs

    conn.sendall(pickle.dumps("connected")) # Begrüßungsnachricht an Client

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
            conn.sendall(pickle.dumps(("mode_set", True)))
        else:
            conn.sendall(pickle.dumps(("invalid_mode", False)))
            return

        # Auf Nachfrage Index senden!
        index_sent = False

        while True:
            data = conn.recv(8192)
            if not data:
                print(f"[DEBUG] Client {player} hat die Verbindung geschlossen.")
                break

            # Auf Anfrage des Index:
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