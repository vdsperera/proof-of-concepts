from playwright.sync_api import sync_playwright

profile_path = "C:\Activities\Chrome_Profiles"

with sync_playwright() as playright:
    browser = playright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        channel="chrome",
        headless=False,
    )
    page = browser.new_page()
    page.goto("https://www.theblock.co/latest-crypto-news")
    input("Browser is open. Press Enter to close...")