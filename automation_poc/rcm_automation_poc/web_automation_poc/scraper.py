import asyncio
import sqlite3
from datetime import datetime
from playwright.async_api import async_playwright

DB_NAME = "claims_status.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            claim_id TEXT,
            status TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(claim_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO claims VALUES (?, ?, ?)", (claim_id, status, datetime.now()))
    conn.commit()
    conn.close()

async def run_scraper():
    init_db()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # Set headless=False to see it work
        page = await browser.new_page()

        try:
            print("Navigating to portal...")
            await page.goto("http://127.0.0.1:5000/login")

            # Login
            print("Attempting login...")
            await page.fill("#user", "admin")
            await page.fill("#pass", "password123")
            await page.click("#login-btn")

            # Check if login failed
            if await page.query_selector("#error"):
                error_text = await page.inner_text("#error")
                print(f"Login Failed: {error_text}")
                return

            print("Login successful. Scraping dashboard...")
            await page.wait_for_selector("#claims-table", timeout=5000)

            # Search and Scrape Status for Claim ID 98765
            claim_id = "98765"
            # Find the row containing the claim ID and get the 3rd column (Status)
            row = await page.query_selector(f"tr:has-text('{claim_id}')")
            if row:
                cells = await row.query_selector_all("td")
                status = await cells[2].inner_text()
                print(f"Claim {claim_id} Status: {status}")
                
                # Save to SQLite
                save_to_db(claim_id, status)
                print(f"Data saved to {DB_NAME}")
            else:
                print(f"Claim ID {claim_id} not found in the table.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())
