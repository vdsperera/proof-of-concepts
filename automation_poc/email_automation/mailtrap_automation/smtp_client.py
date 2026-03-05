import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_smtp_email(
    smtp_server="sandbox.smtp.mailtrap.io",
    smtp_port=2525,
    username=None,
    password=None,
    sender_email="test@example.com",
    receiver_email="kadvsperera@gmail.com",
    subject="Mailtrap SMTP Test",
    body="This is a test email sent via Mailtrap SMTP."
):
    """
    Sends an email using Mailtrap's SMTP sandbox.
    """
    if not username or not password:
        print("Error: SMTP Username and Password are required.")
        return False

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        
        print(f"Email sent successfully to {receiver_email}!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # In a real POC, these would be loaded from .env or config
    # Replace with your Mailtrap credentials
    SMTP_USERNAME = "d1937fdbc2f8c4"
    SMTP_PASSWORD = "f02bfc739344a8"
    
    send_smtp_email(username=SMTP_USERNAME, password=SMTP_PASSWORD)
