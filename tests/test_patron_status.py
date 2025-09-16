import pytest
from library_service import get_patron_status_report

def test_patron_status_not_implemented():
    report = get_patron_status_report("123456")
    assert report == {}
