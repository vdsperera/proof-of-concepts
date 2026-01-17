from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://duckduckgo.com")
    page.fill("input[name=q]", "playright python")
    page.press("input[name=q]", "Enter")
    page.wait_for_load_state("networkidle")
    print("Title:", page.title())
    browser.close()