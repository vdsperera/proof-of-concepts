from playwright.sync_api import sync_playwright

profile_path = "C:\\Activities\\Chrome_Profiles"

# scroll_by_js: step-scroll until bottom, with a short delay between steps
def scroll_by_js(page, step=500, delay=0.2):
    page.evaluate(
        """(step, delay) => new Promise(resolve => {
            let timer = setInterval(() => {
                window.scrollBy(0, step);
                if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, delay * 1000);
        })""",
        # {"step": step, "delay": delay}
    )


def scroll_until_no_change(page, pause_time=1.0, max_iters=30):
    page.evaluate(
        """async (pauseTime, maxIters) => {
            let lastHeight = document.body.scrollHeight;
            for (let i = 0; i < maxIters; i++) {
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(r => setTimeout(r, pauseTime * 1000));
                let newHeight = document.body.scrollHeight;
                if (newHeight === lastHeight) break;
                lastHeight = newHeight;
            }
        }""",
        # {"pauseTime": pause_time, "maxIters": max_iters}
    )


with sync_playwright() as playright:
    browser = playright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        channel="chrome",
        headless=False,
    )
    page = browser.new_page()
    page.goto("https://www.theblock.co/latest-crypto-news")
    # page.wait_for_load_state("networkidle")
    scroll_until_no_change(page)
    # scroll_by_js(page)
    input("Browser is open. Press Enter to close...")

