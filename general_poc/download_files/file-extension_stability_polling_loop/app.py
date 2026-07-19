import os
import time
import shutil
import uuid
from pathlib import Path
from threading import Thread

# =====================================================================
# Setup & Configuration
# =====================================================================
BASE_DIR = Path("general_poc/download_files/file-extension_stability_polling_loop/poc_workspace")
TARGET_DIR = BASE_DIR / "final_cases"

# Clean up any previous runs to ensure reproducibility
if BASE_DIR.exists():
    shutil.rmtree(BASE_DIR)
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Mock database of cases to process
CASES_TO_PROCESS = [
    {"case_id": "CASE-2026-A", "download_duration": 1.5},
    {"case_id": "CASE-2026-B", "download_duration": 0.5},
    {"case_id": "CASE-2026-C", "download_duration": 2.0}
]

# =====================================================================
# Simulation Helper (Simulates a browser downloading a file)
# =====================================================================
def simulate_browser_download(download_folder: Path, case_id: str, duration: float):
    """Simulates the browser dropping a temporary download file and clearing it when finished."""
    time.sleep(0.2)  # Small delay before the download begins
    
    # Browser writes a temporary partial file
    temp_filename = f"document_download_{case_id}.pdf.crdownload"
    temp_file_path = download_folder / temp_filename
    
    print(f"[Browser] Starting network stream: {temp_filename}")
    temp_file_path.write_text("Simulated heavy PDF payload data...")
    
    # Simulate network transfer time
    time.sleep(duration)
    
    # Browser completes download: renames temporary file to final target name
    final_filename = f"document_download_{case_id}.pdf"
    final_file_path = download_folder / final_filename
    temp_file_path.rename(final_file_path)
    print(f"[Browser] Stream finalized: {final_filename}")

# =====================================================================
# Core Logic Execution (The PoC Solution)
# =====================================================================
def process_case_download(case_id: str, download_duration: float):
    print(f"\n[Worker-{case_id}] Launching job loop for Case ID: {case_id}")
    
    # Step 1: Isolate the target landing zone completely using a unique session path
    unique_session_id = str(uuid.uuid4())[:8]
    session_download_dir = BASE_DIR / f"incoming_{case_id}_{unique_session_id}"
    session_download_dir.mkdir(parents=True, exist_ok=True)
    print(f"[Worker-{case_id}] Isolated sandbox created: {session_download_dir.name}")
    
    # Trigger the mock download asynchronously 
    browser_thread = Thread(target=simulate_browser_download, args=(session_download_dir, case_id, download_duration))
    browser_thread.start()
    
    # Step 2: Extension stability polling loop
    timeout = 10
    start_time = time.time()
    final_downloaded_file = None
    
    print(f"[Worker-{case_id}] Polling directory until temporary extensions vanish...")
    while time.time() - start_time < timeout:
        files = list(session_download_dir.glob("*"))
        
        # Check if a file exists and make sure it doesn't contain a temporary browser extension
        if files and not any(f.suffix in ['.crdownload', '.tmp', '.part'] for f in files):
            final_downloaded_file = files[0]
            break
            
        time.sleep(0.3) # Wait before checking the filesystem again
        
    if not final_downloaded_file:
        raise TimeoutError(f"Download timed out or failed for case: {case_id}")
        
    # Step 3: Rename and move atomically to the shared target directory
    file_extension = final_downloaded_file.suffix
    destination_path = TARGET_DIR / f"{case_id}{file_extension}"
    
    # Use shutil.move to safely handle potential cross-device disk volume issues
    shutil.move(str(final_downloaded_file), str(destination_path))
    print(f"[Worker-{case_id}] SUCCESS: Saved and renamed to -> {destination_path.relative_to(BASE_DIR.parent)}")
    
    # Cleanup the temporary isolated sandbox folder
    shutil.rmtree(session_download_dir)
    print(f"[Worker-{case_id}] Cleaned up sandbox folder.")

# =====================================================================
# Demo Main Runner
# =====================================================================
if __name__ == "__main__":
    print("=== STARTING ISOLATED DOWNLOAD DIRECTORY POC ===")
    
    # Run the cases sequentially to cleanly demonstrate the console outputs
    for case_data in CASES_TO_PROCESS:
        process_case_download(case_data["case_id"], case_data["download_duration"])
        
    print("\n=== VERIFYING FINAL TARGET DIRECTORY CONTENTS ===")
    for final_file in TARGET_DIR.glob("*"):
        print(f"Verified File in Destination: {final_file.relative_to(BASE_DIR.parent)}")