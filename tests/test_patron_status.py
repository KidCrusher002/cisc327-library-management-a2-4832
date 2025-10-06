from library_service import get_patron_status_report

def test_invalid_patron():
    result = get_patron_status_report("12")
    assert "error" in result

def test_patron_with_no_records(monkeypatch):
    monkeypatch.setattr("library_service.get_patron_borrowed_books", lambda p: [])
    monkeypatch.setattr("library_service.get_patron_borrow_count", lambda p: 0)
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 0.0})

    class FakeConn:
        def execute(self, q, params): return []
        def close(self): pass
    monkeypatch.setattr("library_service.get_db_connection", lambda: FakeConn())

    result = get_patron_status_report("123456")
    assert result["borrow_count"] == 0
    assert result["total_late_fees"] == 0.0

def test_patron_with_active_and_history(monkeypatch):
    monkeypatch.setattr("library_service.get_patron_borrowed_books", lambda p: [{"book_id": 1, "title": "Book A"}])
    monkeypatch.setattr("library_service.get_patron_borrow_count", lambda p: 1)
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 2.0})

    class FakeConn:
        def execute(self, q, params):
            return [{"book_id": 1, "title": "Book A", "author": "Author A", "borrow_date": "2025-09-01",
                     "due_date": "2025-09-15", "return_date": None}]
        def close(self): pass
    monkeypatch.setattr("library_service.get_db_connection", lambda: FakeConn())

    result = get_patron_status_report("123456")
    assert result["borrow_count"] == 1
    assert result["total_late_fees"] == 2.0
    assert "borrow_history" in result
