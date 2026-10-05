import pytest

from src.file_validation import validate_record


@pytest.fixture
def record():
    return {"transaction_id": "1001", "customer_name": "  Maria Garcia  ",
            "amount": "75.50", "status": " approved "}


def test_normalizes_without_mutating_input(record):
    original = record.copy()
    assert validate_record(record) == {
        "transaction_id": 1001, "customer_name": "Maria Garcia",
        "amount": "75.50", "status": "Approved",
    }
    assert record == original


@pytest.mark.parametrize("field,value", [
    ("transaction_id", "ABC"), ("transaction_id", "0"),
    ("transaction_id", "1.5"), ("customer_name", "  "),
    ("amount", "NOTANUMBER"), ("amount", "NaN"),
    ("amount", "Infinity"), ("amount", "-50"),
    ("amount", "1.001"), ("status", "Unknown"),
    ("status", None),
])
def test_rejects_invalid_values(record, field, value):
    record[field] = value
    with pytest.raises(ValueError):
        validate_record(record)


def test_accepts_zero_amount(record):
    record["amount"] = "0"
    assert validate_record(record)["amount"] == "0.00"


def test_rejects_extra_columns(record):
    record[None] = ["unexpected"]
    with pytest.raises(ValueError, match="columns"):
        validate_record(record)
