"""Utility to read Google Sheets rows, run a sample 3-step process, and mark processed rows as Completed.

Functions:
- get_credentials
- build_sheets_service
- read_sheet_with_headers
- sample_three_step_process
- update_status / batch_update_statuses
- process_sheet (orchestrator)

Example usage in `__main__`.
"""
from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional, Tuple

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_credentials(credentials_path: str = "credentials.json", token_path: str = "token.json") -> Credentials:
    """Return valid OAuth2 Credentials for Google Sheets API (refreshes/stores tokens)."""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return creds


def build_sheets_service(credentials_path: str = "credentials.json", token_path: str = "token.json"):
    """Build and return a Google Sheets API service resource."""
    creds = get_credentials(credentials_path, token_path)
    return build("sheets", "v4", credentials=creds)


def read_sheet_with_headers(spreadsheet_id: str, sheet_name: str, service=None) -> Tuple[List[str], List[Dict[str, str]]]:
    """Read the whole sheet and return (headers, rows) where each row is a dict header->value.

    Assumes first row contains headers. Missing values are returned as empty strings.
    """
    if service is None:
        service = build_sheets_service()
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    values = result.get("values", [])
    if not values:
        return [], []
    headers = [h.strip() for h in values[0]]
    rows = []
    for row_vals in values[1:]:
        # map headers to values, fill missing with ''
        row = {headers[i]: (row_vals[i] if i < len(row_vals) else "") for i in range(len(headers))}
        rows.append(row)
    return headers, rows


def _index_to_column_letter(index: int) -> str:
    """Convert 0-based column index to Excel-style column letter (A, B, ..., AA, AB, ...)."""
    letters = []
    i = index + 1
    while i > 0:
        i, rem = divmod(i - 1, 26)
        letters.append(chr(rem + ord("A")))
    return "".join(reversed(letters))


def sample_three_step_process(row: Dict[str, str]) -> Tuple[bool, Dict[str, str]]:
    """A deterministic simple 3-step process for demo purposes.

    Steps:
    1. Validate: ensure at least one non-empty value exists.
    2. Enrich: create a `processed_at` timestamp and optional `task_key`.
    3. Finalize: produce a `summary` string.

    Returns (success, outputs).
    """
    # Step 1: validation
    if not any(v.strip() for v in row.values()):
        return False, {"reason": "empty_row"}

    # Step 2: enrich
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    task_key = (row.get("id") or row.get("ID") or row.get("name") or row.get("task") or "")

    # Step 3: finalize
    summary = f"Processed {task_key} at {ts}" if task_key else f"Processed at {ts}"
    return True, {"processed_at": ts, "task_key": task_key, "summary": summary}


def update_status(spreadsheet_id: str, sheet_name: str, row_number_1based: int, col_index_0based: int, status: str = "Completed", service=None):
    """Update a single cell (status) identified by sheet, row number and column index."""
    if service is None:
        service = build_sheets_service()
    col_letter = _index_to_column_letter(col_index_0based)
    range_name = f"{sheet_name}!{col_letter}{row_number_1based}"
    body = {"values": [[status]]}
    return service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="RAW", body=body).execute()


def batch_update_statuses(spreadsheet_id: str, sheet_name: str, updates: List[Tuple[int, int, str]], service=None):
    """Batch update multiple cells.

    `updates` is a list of tuples: (row_number_1based, col_index_0based, value)
    """
    if service is None:
        service = build_sheets_service()
    data = []
    for row_num, col_idx, value in updates:
        col_letter = _index_to_column_letter(col_idx)
        rng = f"{sheet_name}!{col_letter}{row_num}"
        data.append({"range": rng, "values": [[value]]})
    body = {"valueInputOption": "RAW", "data": data}
    return service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()


def process_sheet(spreadsheet_id: str, sheet_name: str, status_column_name: str = "status", service=None, logger: Optional[logging.Logger] = None) -> Dict[str, int]:
    """Orchestrate reading rows, running the 3-step process, and marking processed rows as Completed.

    Returns a summary dict with counts: processed, skipped, failed.
    """
    logger = logger or logging.getLogger(__name__)
    if service is None:
        service = build_sheets_service()

    headers, rows = read_sheet_with_headers(spreadsheet_id, sheet_name, service=service)
    if not headers:
        logger.info("Sheet is empty or missing headers")
        return {"processed": 0, "skipped": 0, "failed": 0}

    # find status column (case-insensitive)
    try:
        status_col_idx = next(i for i, h in enumerate(headers) if h.strip().lower() == status_column_name.lower())
    except StopIteration:
        raise ValueError(f"Status column '{status_column_name}' not found in headers: {headers}")

    updates = []  # accumulate updates as (row_num_1based, col_index, value)
    processed = skipped = failed = 0

    for i, row in enumerate(rows):
        sheet_row_number = i + 2  # headers are row 1
        current_status = row.get(headers[status_col_idx], "").strip().lower()
        if current_status == "completed":
            skipped += 1
            continue
        # run sample process
        ok, out = sample_three_step_process(row)
        if ok:
            updates.append((sheet_row_number, status_col_idx, "Completed"))
            processed += 1
            logger.info("Row %s: processed (%s)", sheet_row_number, out.get("summary"))
        else:
            failed += 1
            logger.warning("Row %s: failed (%s)", sheet_row_number, out.get("reason"))

    if updates:
        batch_update_statuses(spreadsheet_id, sheet_name, updates, service=service)
        logger.info("Updated %s rows to Completed", len(updates))

    return {"processed": processed, "skipped": skipped, "failed": failed}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process rows in a Google Sheet and mark them Completed")
    parser.add_argument("--spreadsheet-id", required=True, help="SpreadSheet ID")
    parser.add_argument("--sheet-name", default="Sheet1", help="Sheet name / range (default Sheet1)")
    parser.add_argument("--status-column", default="status", help="Name of the status column (default: status)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    svc = build_sheets_service()
    summary = process_sheet(args.spreadsheet_id, args.sheet_name, status_column_name=args.status_column, service=svc)
    print("Done:", summary)
