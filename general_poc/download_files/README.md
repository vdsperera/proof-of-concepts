# File Download Strategies Proof of Concept

This repository contains three different proof-of-concept (PoC) approaches for handling and capturing file downloads during automation.

## 1. Playwright Native Event Stream Interception
**Location:** [`playwright_native_event stream_interception/app.py`](file:///c:/Activities/Projects/proof-of-concepts/general_poc/download_files/playwright_native_event%20stream_interception/app.py)

This approach leverages Playwright's built-in `page.expect_download()` context manager to natively intercept network download streams.

**How it works:**
- It wraps the action that triggers the download (e.g., clicking a button or navigating to an attachment URL) inside `with page.expect_download():`.
- Playwright automatically pauses execution until the file has completely finished downloading.
- Once complete, it provides a `Download` object that contains metadata (like the suggested filename) and a `.save_as()` method to atomically save the file to your desired destination.

**Pros:**
- Extremely robust and directly integrated into the browser's native network layer.
- No need to guess or poll for completion.
- Handles temporary files and cleanup automatically behind the scenes.

**Cons:**
- Only works if the download triggers standard browser download events. 

---

## 2. File Extension Stability Polling Loop
**Location:** [`file-extension_stability_polling_loop/app.py`](file:///c:/Activities/Projects/proof-of-concepts/general_poc/download_files/file-extension_stability_polling_loop/app.py)

This approach creates an isolated download directory per session/worker and relies on a manual file-system polling loop to detect when a download is finished.

**How it works:**
- The automation is instructed to download files into a dynamically generated, unique directory (e.g., a UUID-named folder).
- A polling loop constantly scans this directory using `time.sleep()`.
- It looks for files with temporary browser extensions indicating an incomplete stream (`.crdownload` for Chrome/Edge, `.part` for Firefox, `.tmp`).
- Once a file exists and no temporary extensions are found in the folder, the script assumes the download has finalized and safely moves the file to the final destination.

**Pros:**
- Agnostic to the automation framework; can be used with Selenium, PyAutoGUI, or complex UI scenarios where native hooks fail.
- Reliable if downloads are properly isolated per-worker to avoid race conditions.

**Cons:**
- Relies on arbitrary timeouts and sleep intervals, which can slow down execution or cause flaky timeouts.
- Requires manual cleanup of the temporary sandbox directories.

---

## 3. Direct Browser-to-Cloud Streaming (S3)
**Location:** [`cloud-pipeline/app.py`](file:///c:/Activities/Projects/proof-of-concepts/general_poc/download_files/cloud-pipeline/app.py)

This approach streams the downloaded file directly from the browser's temporary local cache into AWS S3 (or any other cloud storage) without requiring you to manually save and manage the file on disk.

**How it works:**
- It intercepts the network stream natively using `page.expect_download()`.
- Instead of calling `download.save_as()`, it reads the file bytes directly into memory from Playwright's internal caching location using `download.path()`.
- The raw byte stream is wrapped in a standard `io.BytesIO` object.
- The stream is then uploaded directly to the cloud storage using the SDK (e.g., `boto3.client('s3').upload_fileobj()`) and tagged with relevant metadata.

**Pros:**
- Extremely clean storage footprint; avoids creating permanent files on the host machine.
- Ideal for scalable cloud environments (Docker/Kubernetes) where local persistent disk space is limited or ephemeral.
- Seamlessly injects business context (like Case IDs) as object metadata during the upload pipeline.

**Cons:**
- Requires loading the entire file payload into memory before streaming, which could be problematic for multi-gigabyte files.
- More complex to set up due to the I/O stream wrapping and cloud credentials.
