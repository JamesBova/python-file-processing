import pytest
from src.file_validation import validation_filename


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("transactions_20260930", True),
        ("transactions_20260228", True),
        ("transactions_20260231", False),
        ("transactions_20261301", False),
        ("transactions_2026093", False),
        ("transactions_", False),
        ("transactions_ABCD1234", False),
        ("transactions_20240229", True),
        ("transactions_20230229", False),
        ("transaction_20260930", False),
        ("transactions_20260930_extra", False),
        ("transactions_20260930.csv", False),
        ("", False),
        ("transactions", False),
    ],
)
def test_file_name(filename, expected):
    assert validation_filename(filename) == expected
