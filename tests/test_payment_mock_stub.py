import pytest
from unittest.mock import Mock
from library_service import pay_late_fees, refund_late_fee_payment

# --- PAY LATE FEES TESTS ---

def test_pay_late_fees_success(monkeypatch):
    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "success", "transaction_id": "TX123"}

    # Mock calculate_late_fee_for_book to return a known fee
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 5.0})

    success, msg = pay_late_fees("123456", 1, mock_gateway)

    assert success
    assert "paid successfully" in msg
    mock_gateway.process_payment.assert_called_once_with("123456", 5.0)


def test_pay_late_fees_no_fee(monkeypatch):
    mock_gateway = Mock()
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 0.0})

    success, msg = pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "No outstanding late fee" in msg


def test_pay_late_fees_payment_failure(monkeypatch):
    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "failed", "error": "Declined"}

    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 10.0})

    success, msg = pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Payment failed" in msg


def test_pay_late_fees_exception(monkeypatch):
    mock_gateway = Mock()
    mock_gateway.process_payment.side_effect = Exception("Service unavailable")

    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 8.0})

    success, msg = pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Payment processing error" in msg

def test_pay_late_fees_invalid_patron(monkeypatch):
    mock_gateway = Mock()
    monkeypatch.setattr("library_service.calculate_late_fee_for_book", lambda p, b: {"fee_amount": 5.0})
    success, msg = pay_late_fees("12", 1, mock_gateway)
    assert not success
    assert "Invalid patron ID" in msg
    mock_gateway.process_payment.assert_not_called()



# --- REFUND LATE FEE TESTS ---

def test_refund_success():
    mock_gateway = Mock()
    mock_gateway.refund_payment.return_value = {"status": "success", "refund_id": "RF123"}

    success, msg = refund_late_fee_payment("TX123", 5.0, mock_gateway)
    assert success
    assert "Refund" in msg
    mock_gateway.refund_payment.assert_called_once_with("TX123", 5.0)


def test_refund_invalid_amount():
    mock_gateway = Mock()
    success, msg = refund_late_fee_payment("TX123", -10, mock_gateway)
    assert not success
    assert "Invalid refund amount" in msg


def test_refund_gateway_failure():
    mock_gateway = Mock()
    mock_gateway.refund_payment.return_value = {"status": "failed", "error": "Insufficient funds"}

    success, msg = refund_late_fee_payment("TX123", 10, mock_gateway)
    assert not success
    assert "Refund failed" in msg

def test_refund_invalid_transaction_id():
    mock_gateway = Mock()
    success, msg = refund_late_fee_payment("", 5.0, mock_gateway)
    assert not success
    assert "Invalid transaction ID" in msg
    mock_gateway.refund_payment.assert_not_called()

def test_refund_exceeds_maximum():
    mock_gateway = Mock()
    mock_gateway.refund_payment.return_value = {"status": "failed", "error": "Amount exceeds maximum limit"}
    success, msg = refund_late_fee_payment("TX123", 20.0, mock_gateway)
    assert not success
    assert "Refund failed" in msg


