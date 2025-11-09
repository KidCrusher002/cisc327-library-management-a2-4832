import pytest
from datetime import datetime
from library_service import borrow_book_by_patron
import database  # import the actual module used in library_service.py

def test_borrow_success(monkeypatch):
    fake_book = {"id": 1, "title": "Book A", "available_copies": 2}

    # Patch database functions that are actually called in library_service
    monkeypatch.setattr(database, "get_book_by_id", lambda id: fake_book)
    monkeypatch.setattr(database, "get_patron_borrow_count", lambda p: 2)
    monkeypatch.setattr(database, "insert_borrow_record", lambda p, b, d, due: True)
    monkeypatch.setattr(database, "update_book_availability", lambda b, c: True)

    success, msg = borrow_book_by_patron("123456", 1)
    assert success
    assert "Successfully borrowed" in msg


def test_borrow_invalid_patron():
    success, msg = borrow_book_by_patron("abc", 1)
    assert not success
    assert "Invalid patron ID" in msg


def test_borrow_book_not_found(monkeypatch):
    monkeypatch.setattr(database, "get_book_by_id", lambda id: None)

    success, msg = borrow_book_by_patron("123456", 1)
    assert not success
    assert "Book not found" in msg


def test_borrow_no_copies(monkeypatch):
    monkeypatch.setattr(database, "get_book_by_id", lambda id: {"available_copies": 0})

    success, msg = borrow_book_by_patron("123456", 1)
    assert not success
    assert "not available" in msg


def test_borrow_limit_bug(monkeypatch):
    fake_book = {"id": 1, "title": "Book A", "available_copies": 1}

    monkeypatch.setattr(database, "get_book_by_id", lambda id: fake_book)
    monkeypatch.setattr(database, "get_patron_borrow_count", lambda p: 5)  # Trigger limit
    monkeypatch.setattr(database, "insert_borrow_record", lambda p, b, d, due: True)
    monkeypatch.setattr(database, "update_book_availability", lambda b, c: True)

    success, msg = borrow_book_by_patron("123456", 1)
    assert not success
    assert "maximum borrowing limit" in msg

