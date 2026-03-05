from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/upload")

    page.set_input_files("input[type='file'][id='file-upload']", "C:\\Users\\User\Downloads\\Leonardo_Lightning_XL_realistic_suburban_street_at_dusk_with_f_0.jpg")
    page.click("input[type='submit'][id='file-submit']")

    input("Enter to close..")
    browser.close()