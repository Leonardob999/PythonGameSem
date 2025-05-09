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
        if isinstance(self.p, tuple):
            return self.p[0]  # Der Spieler ist das erste Element des Tuples
        return self.p

    def getB(self):
        if isinstance(self.p, tuple):
            return self.p[1]  # Der Ball ist das zweite Element
        return None  # Kein Ball verfügbar

    def connect(self):
           try:
               self.client.connect(self.addr)
               data = self.client.recv(8192)
               if not data:
                   raise ValueError("No data received from server.")
               return pickle.loads(data)
           except Exception as e:
               print(f"Connection error: {e}")
               return None

    def send(self, data):
        try:
            if data == "disconnect":
                self.client.close()  # Verbindung explizit beenden
                return None
            self.client.send(pickle.dumps(data))
            received = self.client.recv(8192)
            if received:
                return pickle.loads(received)
            else:
                print("No data received from server.")
                return None
        except Exception as e:
            print(f"Error sending data: {e}")
            return None

