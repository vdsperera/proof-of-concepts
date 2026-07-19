from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(accept_downloads=True)
        try:
            with page.expect_download() as download_info:
                page.goto("http://localhost:8000/report.pdf")
            print("Download successful without exception")
        except Exception as e:
            print("Exception raised:", e)
        browser.close()

test()
