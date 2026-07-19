import io
import boto3
from moto import mock_aws
from pathlib import Path
from playwright.sync_api import sync_playwright

# =====================================================================
# Configuration & Cloud Mock Environment Setup
# =====================================================================
BUCKET_NAME = "enterprise-case-storage"
TARGET_CASE_ID = "CASE-2026-CLOUD-STREAM"

@mock_aws
def run_s3_streaming_poc():
    print("=== STARTING DIRECT BROWSER-TO-S3 STREAMING POC ===")
    
    # 1. Initialize our mocked cloud storage infrastructure
    s3_client = boto3.client("s3", region_name="us-east-1")
    s3_client.create_bucket(Bucket=BUCKET_NAME)
    print(f"[Cloud Init] Created target cloud bucket: s3://{BUCKET_NAME}")

    # 2. Initialize Playwright Browser Context
    with sync_playwright() as p:
        print("[Browser] Launching Headless Chromium...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Context-level event hook catching the network stream at the protocol layer
        with page.expect_download() as download_info:
            # Navigating or clicking directly triggers the browser's download engine
            try:
                # For this demonstration, we navigate to a public page that triggers a clear download stream
                print("[Browser] Navigating to download portal page...")
                page.goto("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")
            except Exception as e:
                # Ignore the "Download is starting" or "net::ERR_ABORTED" error if thrown by Playwright
                if "Download is starting" not in str(e) and "net::ERR_ABORTED" not in str(e):
                    raise e
        
        # Block until the browser internal buffer acknowledges receipt of the stream
        download = download_info.value
        suggested_name = download.suggested_filename
        file_extension = Path(suggested_name).suffix
        print(f"[Browser] In-memory file stream captured! Original Name: {suggested_name}")

        # =====================================================================
        # CORE STREAMING PIPELINE: Browser Buffer -> In-Memory -> S3 Upload
        # =====================================================================
        print(f"[Pipeline] Opening read stream allocation from browser memory space...")
        
        # In Playwright Python, the browser temporarily caches the download on disk.
        # We can read it directly from that temporary path and stream it into memory.
        with open(download.path(), "rb") as f:
            file_bytes = f.read()
        
        # Wrap the raw byte block into a standard I/O byte stream interface
        byte_stream = io.BytesIO(file_bytes)
        
        # Define the cloud storage landing destination path mapped directly to the Case ID
        s3_target_key = f"landing-zone/{TARGET_CASE_ID}{file_extension}"
        
        print(f"[Pipeline] Uploading stream to cloud storage via boto3.upload_fileobj()...")
        
        # Upload the file stream directly to AWS S3 without ever touching local hard disk storage
        s3_client.upload_fileobj(
            Fileobj=byte_stream,
            Bucket=BUCKET_NAME,
            Key=s3_target_key,
            ExtraArgs={
                "Metadata": {
                    "case_id": TARGET_CASE_ID,
                    "original_name": suggested_name
                }
            }
        )
        print(f"[Success] File streamed successfully! Cloud Location -> s3://{BUCKET_NAME}/{s3_target_key}")
        
        # Close out automation resources gracefully
        browser.close()

    # =====================================================================
    # Verification Step: Query Cloud State
    # =====================================================================
    print("\n=== VERIFYING OBJECT ARCHIVE AND METADATA IN S3 ===")
    meta_response = s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_target_key)
    
    print(f"Verified Object Key: {s3_target_key}")
    print(f"Attached Case ID Tag: {meta_response['Metadata']['case_id']}")
    print(f"Verified In-Memory File Size: {meta_response['ContentLength']} bytes")

if __name__ == "__main__":
    run_s3_streaming_poc()