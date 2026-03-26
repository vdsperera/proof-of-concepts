from pathlib import Path
import logging
import time
from typing import Dict

from playwright.sync_api import sync_playwright, Page
import pyotp

from .config_manager import get_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def get_totp_code(totp_secret: str) -> str:
    """Return a single 6-digit TOTP code as a string."""
    totp = pyotp.TOTP(totp_secret)
    return totp.now()


def fill_totp_fields(page: Page, code: str) -> None:
    """Fill the 6 TOTP input fields with digits from `code`."""
    if len(code) != 6:
        raise ValueError("TOTP code must be 6 digits")
    for idx, digit in enumerate(code):
        selector = f"input[type='tel'][data-id='{idx}']"
        try:
            page.wait_for_selector(selector, timeout=3000)
            page.fill(selector, digit)
        except Exception:
            logger.exception("Failed to fill TOTP digit %s at selector %s", digit, selector)
            raise


def login_with_password(page: Page, email: str, password: str) -> None:
    """Perform initial email/password login steps on the page."""
    page.goto("https://coinmarketcap.com/")
    page.click("button[data-test='Log In']")
    page.fill("input[type='email']", email)
    page.fill("input[type='password']", password)
    page.click("button[data-test='login-btn']")


def handle_recaptcha_if_present(page: Page, wait_timeout: int = 5000) -> None:
    """Wait briefly for a reCaptcha prompt; if present, block until it's gone."""
    locator = page.locator("div.bcap-text-message-title")
    try:
        locator.wait_for(state="visible", timeout=wait_timeout)
        logger.info("reCaptcha detected — please solve it in the browser.")
        while page.is_visible("div.bcap-text-message-title"):
            time.sleep(0.5)
        logger.info("reCaptcha cleared.")
    except Exception:
        logger.debug("No reCaptcha prompt detected within timeout.")


def login_flow() -> None:
    """Top-level flow: load config, open browser, login, enter TOTP."""
    cfg = get_config()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            page = browser.new_page()
            try:
                login_with_password(page, cfg["email"], cfg["password"])
                handle_recaptcha_if_present(page)
                code = get_totp_code(cfg["totp_secret"])
                fill_totp_fields(page, code)
                page.click("button[class='sc-c0a10c7b-0 brLkHp']")
                logger.info("Login flow completed. Browser will remain open for inspection.")
                input("Press Enter to close the browser...")
            finally:
                try:
                    page.close()
                except Exception:
                    pass
                try:
                    browser.close()
                except Exception:
                    pass
    except Exception:
        logger.exception("Login flow failed.")


if __name__ == "__main__":
    login_flow()