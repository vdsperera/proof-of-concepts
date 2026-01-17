class EmailSender:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = "smtp_connection"
        print("Connected")

    def send(self, to):
        print(f"Sent to {to}")
        self.log(to)

    def log(self, to):
        print(f"Logged {to}")

    def disconnect(self):
        self.conn = None
        print("Disconnected")
