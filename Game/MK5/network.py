import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.settimeout(5)
        self.p = self.connect()  # Spieler laden

    def getP(self):
        if isinstance(self.p, tuple):
            if len(self.p) == 2:
                return self.p
            return (None, self.p)
        return (None, None)

    def getB(self):
        if isinstance(self.p, tuple):
            return self.p[1]
        return None

    def connect(self):
        """Verbindung zum Server herstellen."""
        try:
            self.client.connect(self.addr)
            try:
                data = self.client.recv(8192)
            except socket.timeout:
                # Optional: print("Timeout beim Warten auf Daten vom Server.")
                return None

            if not data:
                raise ValueError("No data received from server.")
            # Optional: print("Verbindung erfolgreich hergestellt.")
            return pickle.loads(data)
        except ConnectionRefusedError:
            print("Verbindung verweigert. Ist der Server gestartet?")
            return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def send(self, data):
        """Daten an den Server senden."""
        try:
            if data == "disconnect":
                # Optional: print("Verbindung wird geschlossen.")
                self.client.close()
                return None

            self.client.send(pickle.dumps(data))
            # Optional: print(f"Daten gesendet: {data}")

            try:
                data = self.client.recv(8192)
                # [DEBUG]-Ausgaben entfernt
                if data:
                    return pickle.loads(data)
                else:
                    # Optional: print("[DEBUG] Keine Daten erhalten.")
                    return None
            except socket.timeout:
                # Optional: print("Zeitüberschreitung beim Warten auf die Serverantwort.")
                return None
        except (ConnectionResetError, BrokenPipeError):
            print("Verbindung zum Server verloren. Wurde die Verbindung geschlossen?")
            return None
        except Exception as e:
            print(f"Error sending data: {e}")
            return None