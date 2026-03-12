from playwright.sync_api import sync_playwright
import pyotp
import json


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

    # wait unitl recaptcha is solved
    print("Please solve the reCaptcha in the opened browser window.")
    while True:
        if page.is_visible("div[class='bcap-text-message-title']"):
            break

    while True:
        if not(page.is_visible("div[class='bcap-text-message-title']")):
            break

    print("reCaptcha solved. Please enter the 2FA code.")

    # enter the 2FA code
    # div class=sc-78e96f85-2 sc-78e96f85-3 cQLkdg clXaOy
    # input type=tel data-id="0"
    # input type=tel data-id="1"
    # input type=tel data-id="2"
    # input type=tel data-id="3"
    # input type=tel data-id="4"
    # input type=tel data-id="5"
    page.fill("input[type='tel'][data-id='0']", get_totp_code()[0])
    page.fill("input[type='tel'][data-id='1']", get_totp_code()[1])
    page.fill("input[type='tel'][data-id='2']", get_totp_code()[2])
    page.fill("input[type='tel'][data-id='3']", get_totp_code()[3])
    page.fill("input[type='tel'][data-id='4']", get_totp_code()[4])
    page.fill("input[type='tel'][data-id='5']", get_totp_code()[5])

    page.click("button[class='sc-c0a10c7b-0 brLkHp']")

    input("Browser is open. Press Enter to close...")


# POC SCOPE
# * login flow is completed
# * basic structure of the code is defined
# * basic exception handling is implemented
# * configuration management is implemented