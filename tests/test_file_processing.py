import csv
from pathlib import Path
import shutil

import pytest

from src.file_processor import process_directory, process_file, write_csv

HEADER = "transaction_id,customer_name,amount,status\n"


def put_input(root, content, name="transactions_20260929.csv"):
    (root / "input").mkdir(exist_ok=True)
    path = root / "input" / name
    path.write_text(content, encoding="utf-8")
    return path


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_sample_batch_routes_and_archives(tmp_path):
    (tmp_path / "input").mkdir()
    for sample in (Path(__file__).resolve().parents[1] / "sample_data").glob("*.csv"):
        shutil.copyfile(sample, tmp_path / "input" / sample.name)
    assert process_directory(tmp_path) == 0
    accepted = sum(len(read_rows(path)) for path in (tmp_path / "output").glob("*.csv"))
    rejected = sum(len(read_rows(path)) for path in (tmp_path / "error").glob("*.csv"))
    assert (accepted, rejected) == (10, 5)
    assert len(list((tmp_path / "archive").glob("*.csv"))) == 2
    assert not list((tmp_path / "input").iterdir())
    assert process_directory(tmp_path) == 0
    assert len(list((tmp_path / "output").glob("*.csv"))) == 2


def test_preserves_rejected_values_and_original_archive(tmp_path):
    content = HEADER + "ABC,  Jennifer  ,90.00,approved\n1001,Alice,10,Pending,extra\n"
    put_input(tmp_path, content)
    assert process_directory(tmp_path) == 0
    rows = read_rows(next((tmp_path / "error").glob("*.csv")))
    assert rows[0]["transaction_id"] == "ABC"
    assert rows[0]["customer_name"] == "  Jennifer  "
    assert rows[0]["error_reason"]
    assert rows[1]["extra_fields"] == "['extra']"
    assert next((tmp_path / "archive").glob("*.csv")).read_text() == content
    assert not list((tmp_path / "output").iterdir())


@pytest.mark.parametrize("name,content", [
    ("transaction_20260929.csv", HEADER),
    ("transactions_20260231.csv", HEADER),
    ("transactions_20260929.csv", "wrong,header\n1,2\n"),
    ("transactions_20260929.csv", HEADER + '1001,"unterminated,10,Approved\n'),
    ("transactions_20260929.csv", ""),
    ("transactions_20260929.csv", HEADER.replace("status", "amount")),
])
def test_quarantines_invalid_files(tmp_path, name, content):
    source = put_input(tmp_path, content, name)
    assert process_directory(tmp_path) == 1
    assert not source.exists()
    assert next((tmp_path / "error").glob("*_failed.csv")).read_text() == content
    assert not list((tmp_path / "archive").iterdir())


def test_invalid_encoding(tmp_path):
    source = put_input(tmp_path, HEADER)
    source.write_bytes(b"\xff\xfeinvalid")
    assert process_directory(tmp_path) == 1
    assert next((tmp_path / "error").glob("*.csv")).read_bytes() == b"\xff\xfeinvalid"


def test_accepts_bom_and_header_only_file(tmp_path):
    put_input(tmp_path, "\ufeff" + HEADER)
    assert process_directory(tmp_path) == 0
    assert len(list((tmp_path / "archive").iterdir())) == 1


def test_archive_failure_rolls_back_outputs(tmp_path):
    source = put_input(tmp_path, HEADER + "1001,Alice,10,Approved\n")
    (tmp_path / "output").mkdir()
    (tmp_path / "error").mkdir()
    # A file where the archive directory should be makes archiving fail.
    (tmp_path / "archive").write_text("blocked", encoding="utf-8")
    with pytest.raises(OSError):
        process_file(source, tmp_path)
    assert source.exists()
    assert not list((tmp_path / "output").iterdir())


def test_continues_after_bad_file_and_ignores_non_csv(tmp_path):
    put_input(tmp_path, HEADER, "bad.csv")
    put_input(tmp_path, HEADER + "1001,Alice,10,Approved\n")
    untouched = put_input(tmp_path, "{}", "transactions.json")
    assert process_directory(tmp_path) == 1
    assert untouched.exists()
    assert len(list((tmp_path / "archive").iterdir())) == 1


def test_existing_output_is_not_overwritten(tmp_path):
    target = tmp_path / "output.csv"
    target.write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        write_csv(target, ("id",), [{"id": 1}])
    assert target.read_text() == "original"
