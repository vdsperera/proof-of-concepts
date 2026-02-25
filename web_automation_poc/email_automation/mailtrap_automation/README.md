# Mailtrap Email Sending POC

This POC demonstrates two primary ways to send emails via Mailtrap using Python.

## Approaches

### 1. SMTP via `smtplib` (`smtp_client.py`)
This approach uses Python's built-in `smtplib` to connect to Mailtrap's SMTP sandbox. It is the most common way to test email functionality in legacy or standard web applications.

- **Pros:**
    - Standard protocol supported by almost all frameworks.
    - No external dependencies (uses built-in `smtplib`).
    - Easy drop-in replacement for production SMTP settings.
- **Cons:**
    - Limited to standard email features.
    - Less efficient for high-volume or complex template handling compared to APIs.

### 2. API via Mailtrap Python SDK (`api_client.py`)
This approach uses the official `mailtrap` Python package to interact with Mailtrap's REST API.

- **Pros:**
    - Native support for Mailtrap features like templates and bulk sending.
    - More robust error handling and response metadata.
    - Better performance for high-concurrency scenarios.
- **Cons:**
    - Requires installing an external dependency (`pip install mailtrap`).
    - API keys need careful management (though the same applies to SMTP credentials).

## Implementation Outline

1.  **Environment Setup**: Install dependencies (`mailtrap`).
2.  **Credential Configuration**: 
    - **SMTP Credentials**: Log in to Mailtrap, go to **Email Sandbox** -> **Inboxes** -> Select your inbox -> **SMTP Settings**.
    - **API Token**: Log in to Mailtrap, go to **Settings** -> **API Tokens**. 
        - Click **"Create Token"**.
        - Select **"Email Sending"** (or **"Domain Sending"**) permissions. 
        - For simplicity in a POC, a token with **"Admin"** or broad **"Sending"** access works best.
3.  **Execution**: Run `smtp_client.py` or `api_client.py` with valid credentials.

## Trade-offs

| Feature | SMTP | API (SDK) |
| :--- | :--- | :--- |
| **Ease of Use** | High (Built-in) | Medium (Requires SDK) |
| **Performance** | Standard | High (Optimized for HTTP) |
| **Features** | Basic | Advanced (Templates, Stats) |
| **Flexibility** | Universal | Service-Specific |

## Pitfalls

-   **Sender Verification**: In production mode, you must verify your domain in Mailtrap. For the Sandbox, you can use any email, but it won't actually reach an external inbox.
-   **Rate Limiting**: Mailtrap has rate limits on both SMTP and API calls. Exceeding these will result in errors.
-   **TLS Version**: Ensure your Python version supports the TLS version required by Mailtrap (usually TLS 1.2+).
-   **Credential Security**: Avoid hardcoding credentials. Use environment variables or secret management tools.
-   **Sandbox Limitation (CRITICAL)**: The Mailtrap **Email Sandbox** is a "dummy" SMTP server. It is designed to capture outgoing emails for testing purposes *without* actually delivering them to the real recipient's inbox. This prevents accidental spamming of real users during development.
-   **Production Sending**: If you need to actually deliver emails to real inboxes, you must use Mailtrap **Email API** (not the Sandbox) and verify your sender domain.
