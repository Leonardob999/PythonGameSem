import socket
from _thread import *

from aiofiles.os import replace

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


players = [Player(0, 425, 25, 150, (255, 255, 255)), Player(950, 425, 25, 150, (255, 255, 255))]
players[0].vel = 6
players[1].vel = 6
ball = Ball(500, 500, 15)
scores = [0, 0]  # Punktestand [Spieler 1, Spieler 2]


def threaded_client(conn, player):
    global ball, scores
    try:
        # Spieler und Ball direkt senden
        conn.send(pickle.dumps((players[player], ball, scores)))  # Spieler, Ball und Punktestand schicken
    except Exception as e:
        print(f"Error sending initial data: {e}")
        conn.close()
        return

    while True:
        try:
            # Empfange Daten vom Spieler
            data = pickle.loads(conn.recv(2048))
            if not data:
                print(f"No data received. Closing connection with player {player}.")
                break

            # Spielerstatus aktualisieren
            players[player] = data

            # Ballbewegung und Torlogik
            point = ball.move(players[0], players[1])
            if point == 1:  # Spieler 1 bekommt einen Punkt
                scores[0] += 1
                ball.reset_position()
            elif point == 2:  # Spieler 2 bekommt einen Punkt
                scores[1] += 1
                ball.reset_position()

            # Pro Spieler unterschiedliche Daten senden
            if player == 0:
                reply = (players[1], ball, scores)
            else:
                reply = (players[0], ball, scores)

            conn.sendall(pickle.dumps(reply))  # Sende Antwort zurück
        except EOFError:
            print("Client disconnected!")
            break
        except Exception as e:
            print(f"Error in thread for player {player}: {e}")
            break

    print(f"Lost connection to player {player}")
    conn.close()






currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1