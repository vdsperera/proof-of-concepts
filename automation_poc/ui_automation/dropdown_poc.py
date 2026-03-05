from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/dropdown")

    page.select_option("#dropdown", "Option 2")

    input("Enter to close..")
    browser.close()