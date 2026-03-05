"""gmail_service.py

Gmail API client (OAuth2) — use `GmailService` for sending mail via Gmail API.

This module replaces the old `gmail_helper.py` and provides:
- `GmailService` class with `send_email()` supporting attachments/cc/bcc
- token storage and refresh handling
- retry with exponential backoff for transient errors

Requirements:
- google-auth, google-auth-oauthlib, google-api-python-client
- `credentials.json` (OAuth client) in working dir for first run

Do not commit `credentials.json` or `token.json` to source control.
"""

import os
import base64
import mimetypes
import logging
import time
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

__all__ = ["GmailService"]


class GmailService:
    """Gmail service client using Gmail API (OAuth2).

    - `credentials_path`: path to OAuth client secrets (credentials.json)
    - `token_path`: where access/refresh token is stored (token.json)
    - `sender`: optional email address to use in the From header (defaults to authenticated user)
    """

    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.json', sender: Optional[str] = None):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.sender = sender
        self.logger = logging.getLogger(__name__)
        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self) -> Credentials:
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token_file:
                token_file.write(creds.to_json())
        return creds

    def send_email(
        self,
        recipients: List[str] | str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html: bool = True,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        retries: int = 3,
    ) -> dict:
        """Send email via Gmail API.

        - recipients: str or list of recipient emails
        - subject: str
        - body: str (HTML if html=True)
        - attachments: list of file paths
        - cc, bcc: optional lists
        - retries: number of retries on transient failures (exponential backoff)

        Returns: API response dict (message metadata)
        """
        if isinstance(recipients, (list, tuple)):
            to_field = ','.join(recipients)
        else:
            to_field = recipients

        message = MIMEMultipart()
        message['To'] = to_field
        message['Subject'] = subject
        if self.sender:
            message['From'] = self.sender
        message.attach(MIMEText(body, 'html' if html else 'plain'))

        if cc:
            message['Cc'] = ','.join(cc)
        if bcc:
            # BCC is not part of headers typically, but we include it for sending
            message['Bcc'] = ','.join(bcc)

        if attachments:
            for path in attachments:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Attachment not found: {path}")
                self._attach_file(message, path)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body_payload = {'raw': raw}

        attempt = 0
        while True:
            try:
                sent = self.service.users().messages().send(userId='me', body=body_payload).execute()
                self.logger.info('Email sent: %s', sent.get('id'))
                return sent
            except HttpError as e:
                status = getattr(e, 'status_code', None) or (e.resp.status if hasattr(e, 'resp') else None)
                # Retry on 429 or 5xx
                if attempt < retries and (status is None or 500 <= int(status) < 600 or int(status) == 429):
                    wait = 2 ** attempt
                    self.logger.warning('Transient error when sending email (status=%s). Retrying in %s seconds...', status, wait)
                    time.sleep(wait)
                    attempt += 1
                    continue
                self.logger.exception('Failed to send email after %s attempts', attempt + 1)
                raise

    def _attach_file(self, message: MIMEMultipart, file_path: str):
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


# Example usage
if __name__ == '__main__':
    # Place OAuth client secrets at `credentials.json` (created in Google Cloud Console)
    g = GmailService(credentials_path='credentials.json', token_path='token.json')
    resp = g.send_email(
        recipients=['j1vidu@gmail.com'],
        subject='Test Email via Gmail API',
        body='<h1>Hello!</h1><p>Sent via Gmail API</p>',
        attachments=None
    )
    print('Sent:', resp.get('id'))
