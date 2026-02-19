from playwright.async_api import async_playwright
import asyncio

async def search(browser, q):
    page = await browser.new_page()
    await page.goto("https://duckduckgo.com")
    await page.fill("input[name=q]", q)
    await page.press("input[name=q]", "Enter")
    await page.wait_for_load_state("networkidle")
    title = await page.title()
    await page.close()
    return title

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        queries = ["playwright python", "asyncio python", "headless browser"]
        results = await asyncio.gather(*(search(browser, q) for q in queries))
        print(results)
        await browser.close()

asyncio.run(main())