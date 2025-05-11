import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.settimeout(5)
        self.connected_message_received = False
        self.connect()  # Verbindung wird aufgebaut

    def connect(self):
        try:
            self.client.connect(self.addr)
            # Begrüßungsnachricht empfangen und ignorieren
            try:
                data = self.client.recv(8192)
                if data:
                    msg = pickle.loads(data)
                    if msg == "connected":
                        self.connected_message_received = True
            except socket.timeout:
                print("Timeout beim Empfang der Begrüßung vom Server.")
        except ConnectionRefusedError:
            print("Verbindung verweigert. Ist der Server gestartet?")
        except Exception as e:
            print(f"Connection error: {e}")

    def send(self, data):
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