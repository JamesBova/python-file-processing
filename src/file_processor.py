"""Read CSV batches, route rejected rows, and archive completed sources."""

import csv
from datetime import datetime
import logging
import shutil

from src.file_validation import REQUIRED_FIELDS, validate_record, validation_filename

LOGGER = logging.getLogger(__name__)


def write_csv(path, fields, rows):
    """Create a new output without overwriting an existing file."""
    handle = path.open("x", encoding="utf-8", newline="")
    try:
        with handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    except OSError:
        path.unlink(missing_ok=True)
        raise


def process_file(source, data_dir):
    """Process one file; malformed files raise ValueError before any output."""
    valid_records = []
    rejected_records = []
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        if reader.fieldnames is None or sorted(reader.fieldnames) != sorted(REQUIRED_FIELDS):
            raise ValueError("CSV header must contain exactly the four required columns")
        for record in reader:
            try:
                valid_records.append(validate_record(record))
            except ValueError as error:
                rejected = {}
                for field in REQUIRED_FIELDS:
                    rejected[field] = record.get(field)
                rejected["extra_fields"] = repr(record[None]) if None in record else ""
                rejected["error_reason"] = str(error)
                rejected_records.append(rejected)
    # One identifier links the output and rejection files to the unchanged archive.
    batch = f"{source.stem}_{datetime.now():%Y%m%d_%H%M%S_%f}"
    created = []
    try:
        if valid_records:
            target = data_dir / "output" / f"{batch}.csv"
            write_csv(target, REQUIRED_FIELDS, valid_records)
            created.append(target)
        if rejected_records:
            target = data_dir / "error" / f"{batch}_rejected.csv"
            write_csv(target, REQUIRED_FIELDS + ["extra_fields", "error_reason"], rejected_records)
            created.append(target)
        shutil.move(str(source), str(data_dir / "archive" / f"{batch}.csv"))
    except OSError:
        # Leave the input available for retry if writing or archiving fails.
        for target in created:
            target.unlink(missing_ok=True)
        raise
    LOGGER.info("%s: accepted=%d rejected=%d; archived", source.name,
                len(valid_records), len(rejected_records))
    return len(valid_records), len(rejected_records)


def process_directory(data_dir):
    """Process top-level CSV files and return the number of failed files."""
    data_dir = data_dir.resolve()
    for name in ("input", "output", "error", "archive"):
        (data_dir / name).mkdir(parents=True, exist_ok=True)
    sources = []
    for path in (data_dir / "input").iterdir():
        if path.is_file() and path.suffix.lower() == ".csv":
            sources.append(path)
    sources.sort()
    failures = 0
    for source in sources:
        try:
            if source.suffix != ".csv" or not validation_filename(source.stem):
                raise ValueError("expected transactions_YYYYMMDD.csv with a valid date")
            process_file(source, data_dir)
        except (ValueError, UnicodeError, csv.Error) as error:
            failures += 1
            LOGGER.error("Rejected file %s: %s", source.name, error)
            target = data_dir / "error" / f"{source.stem}_{datetime.now():%Y%m%d_%H%M%S_%f}_failed.csv"
            try:
                shutil.move(str(source), str(target))
            except OSError as move_error:
                LOGGER.error("Could not move %s: %s", source.name, move_error)
        except OSError as error:
            failures += 1
            LOGGER.error("Could not process %s; input retained for retry: %s", source.name, error)
    LOGGER.info("Batch complete: files=%d failed=%d", len(sources), failures)
    return failures
