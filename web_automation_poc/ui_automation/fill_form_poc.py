from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.w3schools.com/html/html_forms.asp")

    page.fill("input[id='fname']", "Dean")
    page.fill("input[id='lname']", "John")
    
    page.click("input[type='submit']")

    input("Enter to close..")
    browser.close()