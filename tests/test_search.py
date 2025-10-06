from library_service import search_books_in_catalog

def test_search_by_title(monkeypatch):
    monkeypatch.setattr("library_service.get_all_books", lambda: [
        {"title": "Python Crash Course", "author": "Eric", "isbn": "123"},
        {"title": "Flask Web Dev", "author": "Miguel", "isbn": "456"}
    ])
    results = search_books_in_catalog("python", "title")
    assert len(results) == 1

def test_search_by_author(monkeypatch):
    monkeypatch.setattr("library_service.get_all_books", lambda: [
        {"title": "Python Crash Course", "author": "Eric", "isbn": "123"},
        {"title": "Flask Web Dev", "author": "Miguel", "isbn": "456"}
    ])
    results = search_books_in_catalog("miguel", "author")
    assert len(results) == 1

def test_search_by_isbn(monkeypatch):
    monkeypatch.setattr("library_service.get_all_books", lambda: [
        {"title": "Python Crash Course", "author": "Eric", "isbn": "123"}
    ])
    results = search_books_in_catalog("123", "isbn")
    assert len(results) == 1

def test_search_no_match(monkeypatch):
    monkeypatch.setattr("library_service.get_all_books", lambda: [
        {"title": "Python Crash Course", "author": "Eric", "isbn": "123"}
    ])
    results = search_books_in_catalog("999", "isbn")
    assert results == []
