import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "100.101.29.26"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.settimeout(5)
        self.p = None
        self.connect()  # Verbindung wird aufgebaut

    def connect(self):
        """Verbindung zum Server herstellen und direkt 'Modus'-Daten schicken."""
        try:
            self.client.connect(self.addr)
            # Achtung: Der Modus muss vom aufrufenden Code geschickt werden!
            # Daher hier KEIN automatischer Send-Versuch, sondern erst später.
            # Die Methode send() wird später vom Client verwendet, um die Modus-Info zu schicken.
            # Wir empfangen also NICHT sofort etwas.
            # self.p belegen lassen wir durch das erste send() von außen
            pass
        except ConnectionRefusedError:
            print("Verbindung verweigert. Ist der Server gestartet?")
        except Exception as e:
            print(f"Connection error: {e}")

    def send(self, data):
        """Daten an den Server senden und Antwort empfangen."""
        try:
            if data == "disconnect":
                self.client.close()
                return None

            self.client.send(pickle.dumps(data))

            try:
                response = self.client.recv(8192)
                if response:
                    return pickle.loads(response)
                else:
                    return None
            except socket.timeout:
                print("Zeitüberschreitung beim Warten auf die Serverantwort.")
                return None
        except (ConnectionResetError, BrokenPipeError):
            print("Verbindung zum Server verloren. Wurde die Verbindung geschlossen?")
            return None
        except Exception as e:
            print(f"Error sending data: {e}")
            return None

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