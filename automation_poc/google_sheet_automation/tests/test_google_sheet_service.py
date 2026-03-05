import pytest

from google_sheet_automation import google_sheet_service as gss


class FakeValues:
    def __init__(self, response):
        self._response = response
        self.last_batch_body = None
        self.last_update = None

    def get(self, spreadsheetId=None, range=None):
        return self

    def execute(self):
        return self._response

    def batchUpdate(self, spreadsheetId=None, body=None):
        self.last_batch_body = body
        return self

    def update(self, spreadsheetId=None, range=None, valueInputOption=None, body=None):
        self.last_update = dict(range=range, body=body)
        return self


class FakeSpreadsheets:
    def __init__(self, values):
        self._values = values

    def values(self):
        return self._values


class FakeService:
    def __init__(self, response):
        self._values = FakeValues(response)
        self.spreadsheets = lambda: FakeSpreadsheets(self._values)


def test_read_sheet_with_headers_empty():
    svc = FakeService({})
    headers, rows = gss.read_sheet_with_headers("id", "Sheet1", service=svc)
    assert headers == []
    assert rows == []


def test_process_sheet_marks_completed():
    # header + three rows; row 2 has Completed status already
    response = {
        "values": [
            ["id", "task", "status"],
            ["1", "task1", ""],
            ["2", "task2", "Completed"],
            ["3", "", ""]
        ]
    }
    svc = FakeService(response)
    summary = gss.process_sheet("id", "Sheet1", status_column_name="status", service=svc)
    assert summary["processed"] == 2
    assert summary["skipped"] == 1
    # verify that batchUpdate body included two updates (C2 and C4)
    body = svc._values.last_batch_body
    assert body is not None
    ranges = {d["range"] for d in [(x["range"], x["values"]) for x in body["data"]]}
    assert "Sheet1!C2" in ranges
    assert "Sheet1!C4" in ranges
