class EmailSender:
    def __init__(self, limit):
        self.sent_count = 0
        self.limit = limit

    def send(self, to):
        if self.sent_count >= self.limit:
            print("Limit reached")
            return
        self.sent_count += 1
        print(f"Sent to {to}")

sender1 = EmailSender(limit=2)
sender2 = EmailSender(limit=5)

sender1.send("alice@example.com")
sender2.send("bob@example.com")
