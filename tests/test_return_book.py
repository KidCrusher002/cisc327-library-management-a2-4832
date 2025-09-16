import pytest
from library_service import return_book_by_patron

def test_return_not_implemented():
    success, msg = return_book_by_patron("123456", 1)
    assert not success
    assert "not yet implemented" in msg
