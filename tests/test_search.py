import pytest
from library_service import search_books_in_catalog

def test_search_always_empty():
    results = search_books_in_catalog("Book", "title")
    assert results == []
