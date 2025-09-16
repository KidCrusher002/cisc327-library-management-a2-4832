import pytest
from library_service import calculate_late_fee_for_book

def test_late_fee_not_implemented():
    result = calculate_late_fee_for_book("123456", 1)
    assert result is None or "not implemented" in str(result).lower()
