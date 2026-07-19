import os
import shutil
import http.server
import socketserver
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright

# =====================================================================
# Setup & Configuration
# =====================================================================
BASE_DIR = Path(__file__).parent / "playwright_workspace"
TARGET_DIR = BASE_DIR / "final_cases"

# Reset workspace for clean reproducibility
if BASE_DIR.exists():
    shutil.rmtree(BASE_DIR)
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Define our cases to process sequentially inside the single session
CASES = [
    {"case_id": "CASE-2026-X01", "download_url": "http://localhost:8000/report.pdf"},
    {"case_id": "CASE-2026-Y02", "download_url": "http://localhost:8000/data.csv"},
    {"case_id": "CASE-2026-Z03", "download_url": "http://localhost:8000/archive.zip"}
]

# =====================================================================
# Local Mock Server Setup
# =====================================================================
class MockDownloadHandler(http.server.SimpleHTTPRequestHandler):
    """Generates on-the-fly downloadable items with specific content headers."""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        # Force the browser to recognize this network stream as a formal file download
        self.send_header('Content-Disposition', f'attachment; filename="{Path(self.path).name}"')
        self.end_headers()
        self.wfile.write(b"Mock payload content representing raw downloaded bytes.")

def run_mock_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("localhost", 8000), MockDownloadHandler) as httpd:
        httpd.serve_forever()

# Start the local server background thread
server_thread = Thread(target=run_mock_server, daemon=True)
server_thread.start()

# =====================================================================
# Core Playwright Event Stream Interception Logic
# =====================================================================
def process_cases_with_event_interception(case_list, target_path):
    print("\n[Engine] Launching Headless Chromium via Playwright...")
    
    with sync_playwright() as p:
        # Launch a single persistent browser instance
        browser = p.chromium.launch(headless=True)
        # Create a single, shared browser context session
        context = browser.new_context(accept_downloads=True)
        # Open a single automation tab/page to reuse across all cases
        page = context.new_page()
        
        print(f"[Engine] Shared session context established. Processing {len(case_list)} cases...")
        
        for case in case_list:
            case_id = case["case_id"]
            url = case["download_url"]
            
            print(f"\n[Session] Navigating to target portal for Case: {case_id}")
            # Context-level catch: Set up the event listener BEFORE triggering the action
            # This catches the stream instantly at the network protocol layer
            with page.expect_download() as download_info:
                # In a real environment, you would click a UI button here, e.g., page.click("#download-btn")
                # For this PoC, navigating directly to an attachment-header URL triggers the download
                try:
                    page.goto(url)
                except Exception as e:
                    # Ignore the "Download is starting" error if thrown by Playwright
                    if "Download is starting" not in str(e):
                        raise e
            
            # The script blocks here cleanly until Playwright verifies the stream is 100% complete
            download = download_info.value
            
            # Extract the original file extension dynamically from the browser's metadata
            original_filename = download.suggested_filename
            file_extension = Path(original_filename).suffix
            
            # Compute the target file path mapping to the specific Case ID
            final_file_path = target_path / f"{case_id}{file_extension}"
            
            # Atomically save the verified file directly to the destination path
            download.save_as(final_file_path)
            print(f"[Success] Stream captured cleanly! Saved & Renamed -> {final_file_path.relative_to(BASE_DIR.parent)}")
            
        # Clean up the browser resources gracefully upon completion
        browser.close()
        print("\n[Engine] Browser context session safely closed.")

# =====================================================================
# Main Execution Frame
# =====================================================================
if __name__ == "__main__":
    print("=== STARTING PRACTICAL PLAYWRIGHT EVENT INTERCEPTION POC ===")
    
    process_cases_with_event_interception(CASES, TARGET_DIR)
    
    print("\n=== VERIFYING FINAL TARGET DIRECTORY CONTENTS ===")
    for verified_file in TARGET_DIR.glob("*"):
        print(f"Verified File in Destination: {verified_file.relative_to(BASE_DIR.parent)}")