import socket
from _thread import start_new_thread
from player import Player
from ball import Ball
import pickle
import time

DEFAULTS = {
    "player_height": 150,
    "player_width": 25,
    "player_color": (255, 255, 255),
    "ball_radius": 15,
    "max_ball_speed": 9,
    "base_ball_speed": 7,
    "ball_color": (255, 255, 255),
    "max_score": None
}


class GameServer:
    def __init__(self, game_mode, host="0.0.0.0", port=5555):
        self.game_mode = game_mode
        for key, value in DEFAULTS.items():
            if key not in game_mode:
                self.game_mode[key] = value
            else:
                self.game_mode[key] = game_mode[key]
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = [Player(0, 425, 25, 150, (255, 255, 255)), Player(975, 425, 25, 150, (255, 255, 255))]
        self.ball = Ball(500, 400, game_mode.get("ball_radius"), game_mode.get("ball_color"), game_mode.get("max_ball_speed"), game_mode.get("base_ball_speed"))
        self.scores = [0, 0]
        self.currentPlayer = 0
        self.player_inputs = [None, None]
        self.max_score = None
        self.running = False

        # Lambda-Logik teils auf Instanzvariable angepasst
        self.GAME_MODE_APPLIER = {
            "player_height": lambda value: [setattr(p, "height", value) for p in self.players],
            "player_width": lambda value: [setattr(p, "width", value) for p in self.players],
            "player_color": lambda value: [setattr(p, "color", value) for p in self.players],
            "ball_radius": lambda value: setattr(self.ball, "radius", value),
            "max_ball_speed": lambda value: (setattr(self.ball, "vel_x", value), setattr(self.ball, "vel_y", value)),
            "base_ball_speed": lambda value: (setattr(self.ball, "vel_x", value), setattr(self.ball, "vel_y", value)),
            "ball_color": lambda value: setattr(self.ball, "color", value),
            "max_score": lambda value: None
        }

    def apply_game_mode(self, game_mode):
        if not game_mode:
            return
        for key, value in game_mode.items():
            if key in self.GAME_MODE_APPLIER:
                self.GAME_MODE_APPLIER[key](value)
        self.max_score = game_mode["max_score"] if "max_score" in game_mode else DEFAULTS["max_score"]

    def reset_to_defaults(self):
        self.apply_game_mode(DEFAULTS)

    def threaded_client(self, conn, player):
        print("[DEBUG] Threaded Client: Start")
        print("[DEBUG] game_mode ist:", self.game_mode)
        try:
            self.reset_to_defaults()
            print("[DEBUG] Defaults ok")
            self.apply_game_mode(self.game_mode)
            print("[DEBUG] game_mode angewendet")
        except Exception as e:
            print("[ERROR] Initialisierung im Thread fehlgeschlagen:", e)
        conn.sendall(pickle.dumps("connected"))
        print("[DEBUG] Begrüßung versendet")

        try:
            print(f"[DEBUG] Client {player} verbunden. Starte Spiel-Loop...")

            index_sent = False

            while True:
                data = conn.recv(8192)
                if not data:
                    print(f"[DEBUG] Client {player} hat die Verbindung geschlossen.")
                    break
                # Daten vom Client laden (z.B. Spielerbewegung)
                try:
                    loaded = pickle.loads(data)
                except Exception:
                    continue

                # Der Client fragt nach seinem Index
                if loaded == {} and not index_sent:
                    conn.sendall(pickle.dumps(player))
                    index_sent = True
                    continue

                # Spielerbewegung empfangen
                if isinstance(loaded, dict) and 'y' in loaded:
                    self.player_inputs[player] = loaded

                # Spieler-Logik
                if any(self.player_inputs):
                    if self.player_inputs[0] is not None:
                        self.players[0].y = self.player_inputs[0]['y']
                    if self.player_inputs[1] is not None:
                        self.players[1].y = self.player_inputs[1]['y']
                    punkt = self.ball.move(self.players[0], self.players[1])

                    if punkt == 1:
                        self.scores[0] += 1
                        self.ball.reset_position()
                    elif punkt == 2:
                        self.scores[1] += 1
                        self.ball.reset_position()

                # Antwort an den Client bauen
                other_player = self.players[1] if player == 0 else self.players[0]
                game_over = False

                if self.max_score is not None:
                    if self.scores[0] >= self.max_score:
                        game_over = "Player 1 gewinnt!"
                    elif self.scores[1] >= self.max_score:
                        game_over = "Player 2 gewinnt!"

                response = pickle.dumps(
                    (self.players, player, self.ball, self.scores, game_over)
                )
                conn.sendall(response)

                time.sleep(1 / 60.0)
        except Exception as e:
            print(f"[ERROR] Fehler bei Client {player}: {e}")
        finally:
            conn.close()
            print(f"[DEBUG] Verbindung zu Client {player} geschlossen.")

    def stop(self):
        print("Server wird beendet...")
        self.running = False
        self.s.close()

    def start(self):
        try:
            self.s.bind((self.host, self.port))
            print(f"[DEBUG] Server gestartet auf {self.host}:{self.port}")
        except socket.error as e:
            print(f"[ERROR] Fehler beim Binden: {e}")
            return

        self.s.listen(2)
        print("Waiting for a connection, Server Started")
        self.running = True

        while self.running:
            try:
                conn, addr = self.s.accept()
                print(f"[DEBUG] Verbunden mit: {addr}")
                start_new_thread(self.threaded_client, (conn, self.currentPlayer))
                self.currentPlayer += 1
            except Exception as e:
                print(f"[ERROR] Fehler beim Akzeptieren einer Verbindung: {e}")
                break

        self.s.close()
        print("[DEBUG] Server gestoppt.")

    def stop(self):
        self.running = False
        self.s.close()