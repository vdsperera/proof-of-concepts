# gmail_service_functional.py
import os
import base64
import mimetypes
import time
import logging
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_credentials(credentials_path: str = 'credentials.json', token_path: str = 'token.json') -> Credentials:
    """Return valid OAuth2 Credentials, storing refreshing tokens in `token_path`."""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
    return creds


def build_service(credentials_path: str = 'credentials.json', token_path: str = 'token.json'):
    """Build and return a Gmail API service resource."""
    creds = get_credentials(credentials_path, token_path)
    return build('gmail', 'v1', credentials=creds)


def create_raw_message(
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None,
    html: bool = True,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    sender: Optional[str] = None,
) -> str:
    """Construct a base64-url-safe encoded raw message string suitable for Gmail API."""
    to_field = ','.join(recipients) if isinstance(recipients, (list, tuple)) else recipients
    message = MIMEMultipart()
    message['To'] = to_field
    message['Subject'] = subject
    if sender:
        message['From'] = sender
    if cc:
        message['Cc'] = ','.join(cc)
    if bcc:
        message['Bcc'] = ','.join(bcc)
    message.attach(MIMEText(body, 'html' if html else 'plain'))

    if attachments:
        for path in attachments:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Attachment not found: {path}")
            _attach_file(message, path)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return raw


def _attach_file(message: MIMEMultipart, file_path: str):
    """Attach a file to the MIME message (internal helper)."""
    ctype, encoding = mimetypes.guess_type(file_path)
    if ctype is None:
        maintype, subtype = 'application', 'octet-stream'
    else:
        maintype, subtype = ctype.split('/', 1)
    with open(file_path, 'rb') as f:
        part = MIMEBase(maintype, subtype)
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{basename(file_path)}"')
    message.attach(part)


def send_raw_message(service, raw: str, user_id: str = 'me', retries: int = 3, logger: Optional[logging.Logger] = None) -> dict:
    """Send a previously built raw message with retry logic."""
    logger = logger or logging.getLogger(__name__)
    attempt = 0
    while True:
        try:
            body = {'raw': raw}
            resp = service.users().messages().send(userId=user_id, body=body).execute()
            logger.info('Email sent: %s', resp.get('id'))
            return resp
        except HttpError as e:
            status = getattr(e, 'status_code', None) or (e.resp.status if hasattr(e, 'resp') else None)
            if attempt < retries and (status is None or 500 <= int(status) < 600 or int(status) == 429):
                wait = 2 ** attempt
                logger.warning('Transient error when sending email (status=%s). Retrying in %s seconds...', status, wait)
                time.sleep(wait)
                attempt += 1
                continue
            logger.exception('Failed to send email after %s attempts', attempt + 1)
            raise


def send_email(
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None,
    html: bool = True,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    sender: Optional[str] = None,
    credentials_path: str = 'credentials.json',
    token_path: str = 'token.json',
    service=None,
    retries: int = 3,
    logger: Optional[logging.Logger] = None,
) -> dict:
    """
    High-level functional send_email().

    - If `service` is provided it will be used (useful for testing).
    - Otherwise `build_service(credentials_path, token_path)` will be called.
    """
    logger = logger or logging.getLogger(__name__)
    if service is None:
        service = build_service(credentials_path, token_path)
    raw = create_raw_message(recipients, subject, body, attachments, html, cc, bcc, sender)
    return send_raw_message(service, raw, retries=retries, logger=logger)


# Example usage
if __name__ == '__main__':
    # Place OAuth client secrets at `credentials.json` (created in Google Cloud Console)
    resp = send_email(
        recipients=['j1vidu@gmail.com'],
        subject='Test Email via Gmail API',
        body='<h1>Hello!</h1><p>Sent via Gmail API</p>',
        attachments=None
    )
    print('Sent:', resp.get('id'))