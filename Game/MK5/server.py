import socket
from _thread import *
from player import Player
from ball import Ball
import pickle

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

# Initialisierte Spieler und Ball
players = [Player(0, 425, 25, 150, (255, 255, 255)), Player(950, 425, 25, 150, (255, 255, 255))]
ball = Ball(500, 500, 15)

# Globale Variablen
scores = [0, 0]  # Punktestand [Spieler 1, Spieler 2]
currentPlayer = 0
game_config = None  # Spielkonfiguration (durch Spieler 1 festgelegt)

def threaded_client(conn, player):
    global ball, scores, players, currentPlayer, game_config

    try:
        # Spieler 1 darf die Spielkonfiguration setzen, sofern nicht vorhanden
        if player == 0 and game_config is None:
            conn.send(pickle.dumps(("config_required", None)))  # Senden von config_required an Spieler 1
        else:
            conn.send(pickle.dumps(("config_set", (players[player], ball, scores, None))))  # Senden der Konfiguration an Spieler 2

    except Exception as e:
        print(f"Error sending initial data: {e}")
        conn.close()
        return

    while True:
        try:
            data = pickle.loads(conn.recv(8192))
            if not data:
                break

            if data == "disconnect":
                print(f"Player {player} disconnected.")
                break

            players[player] = data

            point = ball.move(players[0], players[1])
            if point == 1:
                scores[0] += 1
                ball.reset_position()
            elif point == 2:
                scores[1] += 1
                ball.reset_position()

            game_over = None
            if scores[0] >= 3:
                game_over = "Player 1 gewinnt!"
            elif scores[1] >= 3:
                game_over = "Player 2 gewinnt!"

            if player == 0:
                reply = (players[1], ball, scores, game_over)
            else:
                reply = (players[0], ball, scores, game_over)

            conn.sendall(pickle.dumps(reply))

            if game_over:  # Wenn das Spiel endet
                print(game_over)
                break

        except Exception:
            break

    print(f"Lost connection to player {player}")
    conn.close()

    # Spieler entfernen und prüfen, ob das Spiel zurückgesetzt werden soll
    players[player] = None
    currentPlayer -= 1  # Spieleranzahl verringern
    if all(p is None for p in players):  # Wenn alle Spieler weg sind
        scores = [0, 0]  # Punktestand zurücksetzen
        ball.reset_position()
        players[0] = Player(0, 425, 25, 150, (255, 255, 255))  # Spieler zurücksetzen
        players[1] = Player(950, 425, 25, 150, (255, 255, 255))
        game_config = None  # Konfiguration zurücksetzen
        print("Game state reset. Ready for new players.")

while True:
    conn, addr = s.accept()
    if currentPlayer >= 2:
        print(f"Connection refused: Too many players ({addr})")
        conn.close()
        continue

    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1