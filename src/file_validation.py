"""Filename and record validation shared by the pipeline and tests."""

from datetime import datetime

REQUIRED_FIELDS = ["transaction_id", "customer_name", "amount", "status"]
ALLOWED_STATUSES = ["Approved", "Pending", "Declined"]


def validation_filename(filename) -> bool:
    """Validate a transactions_YYYYMMDD stem, including its calendar date."""
    parts = filename.split("_")
    if len(parts) != 2 or parts[0] != "transactions":
        return False
    date_text = parts[1]
    if len(date_text) != 8 or not date_text.isascii() or not date_text.isdigit():
        return False
    try:
        datetime(int(date_text[:4]), int(date_text[4:6]), int(date_text[6:]))
    except ValueError:
        return False
    return True


def validate_record(record):
    """Return a normalized copy, or raise ValueError with a rejection reason."""
    if None in record:
        raise ValueError("row has missing or extra columns")
    cleaned = {}
    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if value is None:
            raise ValueError("row has missing or extra columns")
        value = value.strip()
        if value == "":
            raise ValueError(f"missing required value: {field}")
        cleaned[field] = value
    id_text = cleaned["transaction_id"]
    if not id_text.isascii() or not id_text.isdigit():
        raise ValueError("transaction_id must be a positive integer")
    transaction_id = int(id_text)
    if transaction_id <= 0:
        raise ValueError("transaction_id must be a positive integer")
    try:
        amount = float(cleaned["amount"])
    except ValueError:
        raise ValueError("amount must be numeric")
    # This comparison also rejects NaN and infinity without another module.
    if not 0 <= amount < float("inf"):
        raise ValueError("amount must be finite and non-negative")
    amount_parts = cleaned["amount"].split(".")
    if len(amount_parts) > 2:
        raise ValueError("amount must be numeric")
    if len(amount_parts) == 2 and len(amount_parts[1]) > 2:
        raise ValueError("amount must have at most two decimal places")
    for part in amount_parts:
        if not part.isascii() or not part.isdigit():
            raise ValueError("amount must contain digits and an optional decimal point")
    status = cleaned["status"].strip().capitalize()
    if status not in ALLOWED_STATUSES:
        raise ValueError("status must be Approved, Pending, or Declined")
    return {
        "transaction_id": transaction_id,
        "customer_name": cleaned["customer_name"],
        "amount": f"{amount:.2f}",
        "status": status,
    }
