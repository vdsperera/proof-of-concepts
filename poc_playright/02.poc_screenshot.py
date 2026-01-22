from playwright.sync_api import sync_playwright

def take_screenshot(url="https:www.duckduckgo.com", headless=False, keep_open=False):
    with sync_playwright() as playright:
        browser = playright.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path="poc_playright/screenshot.png")
        print("Saved screenshot.png")
        if keep_open:
            input("Browser is open. Press Enter to close...")
        browser.close()

if __name__ == "__main__":
    take_screenshot(url="https://www.cricbuzz.com/", keep_open=True)
