import mailtrap as mt

def send_api_email(
    api_token=None,
    sender_email="test@example.com",
    sender_name="Mailtrap Test",
    receiver_email="kadvsperera@gmail.com",
    subject="Mailtrap API Test",
    body="This is a test email sent via Mailtrap API SDK."
):
    """
    Sends an email using the Mailtrap Python SDK.
    Note: Requires 'mailtrap' package to be installed.
    """
    if not api_token:
        print("Error: Mailtrap API Token is required.")
        return False

    client = mt.MailtrapClient(token=api_token)

    # Note: For Sandbox, the sender domain usually needs to be 'mailtrap.io' 
    # or a verified domain for production sending.
    mail = mt.Mail(
        sender=mt.Address(email=sender_email, name=sender_name),
        to=[mt.Address(email=receiver_email)],
        subject=subject,
        text=body,
    )

    try:
        client.send(mail)
        print(f"API Email sent successfully to {receiver_email}!")
        return True
    except Exception as e:
        print(f"Failed to send API email: {e}")
        return False

if __name__ == "__main__":
    # Replace with your actual Mailtrap API Token
    API_TOKEN = "5b0c77281b1d09b3287c332cae4e716e"
    
    # Example usage
    send_api_email(api_token=API_TOKEN)
