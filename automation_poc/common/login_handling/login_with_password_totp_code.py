from playwright.sync_api import sync_playwright
import pyotp


with sync_playwright() as playright:
    browser = playright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://coinmarketcap.com/")
    page.click("button[data-test='Log In']")
    page.fill("input[type='email']", "j1vidu@gmail.com")
    page.fill("input[type='password']", "BJx@QrmkC42%5AW&")
    page.click("button[data-test='login-btn']")


    input("Browser is open. Press Enter to close...")


# secret = "TMMIMUN4B6HLXSOTQIOHLPSTF5DYRCOX"  # base32
# totp = pyotp.TOTP(secret)
# print(totp.now())  # 6-digit code (default)

