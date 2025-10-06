import pytest
from datetime import datetime, timedelta
from library_service import return_book_by_patron

def test_valid_return(monkeypatch):
    # Fake book + DB operations
    fake_book = {"id": 1, "title": "Book A", "available_copies": 0}

    monkeypatch.setattr("library_service.get_book_by_id", lambda b: fake_book)
    monkeypatch.setattr("library_service.update_borrow_record_return_date", lambda p, b, d: True)
    monkeypatch.setattr("library_service.update_book_availability", lambda b, c: True)
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 0.0, "days_overdue": 0, "status": "On time"})

    success, msg = return_book_by_patron("123456", 1)
    assert success
    assert "returned successfully" in msg

def test_return_invalid_patron():
    success, msg = return_book_by_patron("12", 1)
    assert not success
    assert "Invalid patron ID" in msg

def test_return_nonexistent_book(monkeypatch):
    monkeypatch.setattr("library_service.get_book_by_id", lambda b: None)
    success, msg = return_book_by_patron("123456", 1)
    assert not success
    assert "Book not found" in msg

def test_return_with_late_fee(monkeypatch):
    fake_book = {"id": 1, "title": "Book A", "available_copies": 0}
    monkeypatch.setattr("library_service.get_book_by_id", lambda b: fake_book)
    monkeypatch.setattr("library_service.update_borrow_record_return_date", lambda p, b, d: True)
    monkeypatch.setattr("library_service.update_book_availability", lambda b, c: True)
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 5.0, "days_overdue": 10, "status": "Overdue"})

    success, msg = return_book_by_patron("123456", 1)
    assert success
    assert "Late fee" in msg
