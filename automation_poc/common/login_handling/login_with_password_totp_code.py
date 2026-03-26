from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
import pyotp
import json

""" 
POC SCOPE

* login flow(enter email and password, wait until reCaptcha
* is solved manually, enter 2FA code) is completed- DONE
* basic structure of the code is defined - DONE
* basic exception handling is implemented - IN PROGRESS
* configuration management is implemented - DONE
"""

with open("automation_poc\\common\\login_handling\\config.json") as f:
    config = json.load(f)


def get_totp_code(is_array=False):
    totp = pyotp.TOTP(config["totp_secret"])
    if not is_array:
        return totp.now()  # 6-digit code (default)
    else:
        return totp.now().split()  # 6-digit code (default)


with sync_playwright() as playright:
    browser = playright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://coinmarketcap.com/")
    page.click("button[data-test='Log In']")
    page.fill("input[type='email']", config["email"])
    page.fill("input[type='password']", config["password"])
    page.click("button[data-test='login-btn']")

    """
    reCaptcha is sometimes required to be solved before
    entering the 2FA code, and sometimes not. So it
    should be handled in both cases.    
    """

    locator = page.locator("div.bcap-text-message-title")

    try:
        locator.wait_for(state="visible", timeout=5000)

        # If we reach here, element appeared → do next step
        print("Have to solve the reCaptcha first.")

        while True:
            if not(page.is_visible("div[class='bcap-text-message-title']")):
                break
    except TimeoutError:
        print("No need to solve the reCaptcha first.")  

    # here I think totp can be expired while filling the fields
    page.fill("input[type='tel'][data-id='0']", get_totp_code()[0])
    page.fill("input[type='tel'][data-id='1']", get_totp_code()[1])
    page.fill("input[type='tel'][data-id='2']", get_totp_code()[2])
    page.fill("input[type='tel'][data-id='3']", get_totp_code()[3])
    page.fill("input[type='tel'][data-id='4']", get_totp_code()[4])
    page.fill("input[type='tel'][data-id='5']", get_totp_code()[5])

    page.click("button[class='sc-c0a10c7b-0 brLkHp']")

    input("Browser is open. Press Enter to close...")
