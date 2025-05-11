import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()  # Spieler laden

    def getP(self):
        # Aktuelle Daten prüfen und Struktur sicherstellen
        if isinstance(self.p, tuple):
            if len(self.p) == 2:  # Überprüfen, ob es aus zwei Werten besteht
                return self.p  # Rückgabe eines Tuples mit (Status, Daten)
            return (None, self.p)  # Status ist None, weil keine Konfiguration vorliegt
        return (None, None)  # Keine gültigen Daten enthalten

    def getB(self):
        if isinstance(self.p, tuple):
            return self.p[1]  # Der Ball ist das zweite Element
        return None  # Kein Ball verfügbar

    def connect(self):
        """Verbindung zum Server herstellen."""
        try:
            self.client.connect(self.addr)
            data = self.client.recv(8192)
            if not data:
                raise ValueError("No data received from server.")
            print("Verbindung erfolgreich hergestellt.")
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
                print("Verbindung wird geschlossen.")
                self.client.close()  # Verbindung explizit beenden
                return None

            self.client.send(pickle.dumps(data))
            print(f"Daten gesendet: {data}")

            received = self.client.recv(8192)
            if received:
                decoded_data = pickle.loads(received)
                print(f"Antwort vom Server: {decoded_data}")
                return decoded_data
            else:
                print("Keine Antwort vom Server erhalten.")
                return None
        except (ConnectionResetError, BrokenPipeError):
            print("Verbindung zum Server verloren. Wurde die Verbindung geschlossen?")
            return None
        except Exception as e:
            print(f"Error sending data: {e}")
            return None