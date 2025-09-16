import pytest
from library_service import add_book_to_catalog

def test_add_book_success(monkeypatch):
    monkeypatch.setattr("library_service.get_book_by_isbn", lambda i: None)
    monkeypatch.setattr("library_service.insert_book", lambda t, a, i, tc, ac: True)
    success, msg = add_book_to_catalog("Good Title", "Author", "1234567890123", 3)
    assert success
    assert "successfully added" in msg

def test_add_book_missing_title():
    success, msg = add_book_to_catalog("", "Author", "1234567890123", 2)
    assert not success
    assert "Title is required" in msg

def test_add_book_long_author():
    author = "A" * 101
    success, msg = add_book_to_catalog("Book", author, "1234567890123", 2)
    assert not success
    assert "less than 100 characters" in msg

def test_add_book_duplicate_isbn(monkeypatch):
    monkeypatch.setattr("library_service.get_book_by_isbn", lambda i: {"id": 1})
    success, msg = add_book_to_catalog("Book", "Author", "1234567890123", 2)
    assert not success
    assert "already exists" in msg
