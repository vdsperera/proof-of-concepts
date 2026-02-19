from playwright.sync_api import sync_playwright

profile_path = "C:\\Activities\\Chrome_Profiles"
website_url = "https://portal.pi2.network/"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        channel="chrome",
        headless=False,
    )
    page = browser.new_page()
    page.goto(website_url)

    # login_button = page.locator()
    login_button_container = page.locator("div.p-4.border-t.border-gray-800")
    login_button_container.get_by_role("button", name="Login").click()

    # page.locator('//div[contains(@class, "p-4 border-t border-gray-800")]//button[normalize-space(text())="Login"]').click()
    # page.get_by_placeholder("you@example.com").fill("tradevidu@yahoo.com")
    # page.get_by_text("Send Code").click()

    input("Browser is open. Press Enter to close...")

def login():
    pass

def request_login_code():
    pass

def extract_login_code():
    pass
