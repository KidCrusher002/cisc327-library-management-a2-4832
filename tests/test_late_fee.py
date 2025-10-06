from datetime import datetime, timedelta
from library_service import calculate_late_fee_for_book

def test_no_borrow_record(monkeypatch):
    def fake_conn():
        class Fake:
            def execute(self, q, params):
                return type("", (), {"fetchone": lambda s: None})()
            def close(self): pass
        return Fake()
    monkeypatch.setattr("library_service.get_db_connection", fake_conn)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["status"] == "No borrow record found"

def test_on_time_return(monkeypatch):
    now = datetime.now()
    record = {"borrow_date": now.isoformat(), "due_date": now.isoformat(), "return_date": now.isoformat()}

    def fake_conn():
        class Fake:
            def execute(self, q, params): return type("", (), {"fetchone": lambda s: record})()
            def close(self): pass
        return Fake()
    monkeypatch.setattr("library_service.get_db_connection", fake_conn)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 0.0

def test_three_days_late(monkeypatch):
    now = datetime.now()
    record = {"borrow_date": now.isoformat(), "due_date": (now - timedelta(days=3)).isoformat(), "return_date": now.isoformat()}

    def fake_conn():
        class Fake:
            def execute(self, q, params): return type("", (), {"fetchone": lambda s: record})()
            def close(self): pass
        return Fake()
    monkeypatch.setattr("library_service.get_db_connection", fake_conn)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 1.5

def test_ten_days_late(monkeypatch):
    now = datetime.now()
    record = {"borrow_date": now.isoformat(), "due_date": (now - timedelta(days=10)).isoformat(), "return_date": now.isoformat()}

    def fake_conn():
        class Fake:
            def execute(self, q, params): return type("", (), {"fetchone": lambda s: record})()
            def close(self): pass
        return Fake()
    monkeypatch.setattr("library_service.get_db_connection", fake_conn)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 8.5

def test_fee_cap(monkeypatch):
    now = datetime.now()
    record = {"borrow_date": now.isoformat(), "due_date": (now - timedelta(days=50)).isoformat(), "return_date": now.isoformat()}

    def fake_conn():
        class Fake:
            def execute(self, q, params): return type("", (), {"fetchone": lambda s: record})()
            def close(self): pass
        return Fake()
    monkeypatch.setattr("library_service.get_db_connection", fake_conn)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 15.0
