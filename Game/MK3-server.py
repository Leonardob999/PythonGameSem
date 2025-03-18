import socket
import threading
import time

# Server-Konfiguration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# Spielfeldgrößen
WIDTH = 800
HEIGHT = 600

# Ball- und Schläger-Eigenschaften
BALL_SPEED = 5
PADDLE_SPEED = 10


# Funktion zur Handhabung der Client-Verbindung
def handle_client(client_socket, addr):
    print(f"Neuer Spieler verbunden: {addr}")

    # Initialisierung der Positionen und Bewegungen
    paddle_left = HEIGHT // 2 - 50
    paddle_right = HEIGHT // 2 - 50
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

    while True:
        try:
            # Daten empfangen
            data = client_socket.recv(1024)
            if not data:
                break
            # Verarbeitung der Eingabedaten (Schlägerbewegung)
            paddle_left = int(data.decode())

            # Ball-Bewegung
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball-Kollision mit den oberen und unteren Rändern
            if ball_y <= 0 or ball_y >= HEIGHT:
                ball_dy = -ball_dy

            # Kollision mit den Schlägern
            if (ball_x <= 20 and paddle_left <= ball_y <= paddle_left + 100) or (
                    ball_x >= WIDTH - 20 and paddle_right <= ball_y <= paddle_right + 100):
                ball_dx = -ball_dx

            # Ball verlässt das Spielfeld
            if ball_x <= 0 or ball_x >= WIDTH:
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Reset Ball-Position

            # Senden des Spielstatus an den Client
            game_data = f"{ball_x},{ball_y},{paddle_left},{paddle_right}"
            client_socket.send(game_data.encode())

        except:
            break

    client_socket.close()


# Server starten
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(2)  # Maximale Anzahl der Clients
    print(f"Server gestartet auf {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()


start_server()
