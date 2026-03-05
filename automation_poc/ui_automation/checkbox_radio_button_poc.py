from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.w3schools.com/html/html_forms.asp")

    # checkbox selection
    page.check("input[type='checkbox'][id='vehicle1']")

    # radio button selection
    page.check("input[type='radio'][id='html']")

    input("Entet to close..")
    browser.close()