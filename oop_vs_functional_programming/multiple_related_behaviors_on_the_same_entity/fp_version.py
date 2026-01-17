conn = None

def connect():
    global conn
    conn = "smtp_connection"
    print("Connected")

def send_email(to):
    print(f"Sent to {to}")

def log_email(to):
    print(f"Logged {to}")

def disconnect():
    global conn
    conn = None
    print("Disconnected")
