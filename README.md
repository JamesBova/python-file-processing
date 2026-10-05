# Python Transaction File Processing

A learning and portfolio project that turns daily transaction CSV files into validated datasets, separates rejected records, and archives the original inputs. It demonstrates a small local batch pipeline using readable Python and the standard library.

## Data flow

```text
input/transactions_YYYYMMDD.csv
    -> validate filename and CSV schema
    -> validate and normalize each record
        -> output/ : accepted records
        -> error/  : rejected records with reasons
    -> archive/   : unchanged original file

Invalid filenames, headers, CSV syntax, or encoding -> error/*_failed.csv
File-access failures -> logged; input retained for retry
```

Completed files share a batch identifier made from the input stem and local timestamp, including microseconds. Output files are created only when they have records. A header-only file is archived without producing output. Files with row rejections are still completed and archived.

## Technologies and skills

- Python 3.10+; `csv`, `pathlib`, `shutil`, `logging`, and `datetime`.
- CSV ingestion, schema checks, data cleansing, record-level rejection, and source traceability.
- Numeric conversion and validation using the training's existing `int` and `float` approach.
- Portable file paths, explicit UTF-8 encoding, and contextual error reporting.
- pytest tests with ordinary fixtures and parameterized examples, including malformed inputs and archive failures.

No database, cloud service, credentials, environment variables, or `.env` file is required. `requirements.txt` preserves the original training package versions: colorama, iniconfig, packaging, pluggy, Pygments, and pytest. The pipeline itself uses only the standard library. No additional packages were introduced.

## Repository structure

```text
src/
  main.py                command-line interface
  file_processor.py      batch processing and file routing
  file_validation.py     filename and record rules
sample_data/             two reusable CSV examples
examples/                earlier file-handling lessons
  data/                  lesson fixtures and previous demonstration outputs
tests/                  pipeline tests (at repository root)
requirements.txt         original training packages
pytest.ini               test discovery configuration
```

The `input`, `output`, `error`, and `archive` folders are created when the pipeline runs and are ignored by Git. Sample files are copied into input so running the demonstration does not consume the committed fixtures. Earlier learning scripts remain in `examples` and run in temporary directories, so they do not overwrite repository files.

## Installation

Clone this repository and open a terminal in its root folder. Use your repository's URL in place of the placeholder:

```sh
git clone <your-repository-url>
cd Python-File-Processing
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```sh
source .venv/bin/activate
```

Then install the original training packages:

```sh
python -m pip install -r requirements.txt
```

On Windows, if `python` is unavailable, use `py -3` to create the environment. Install Python if neither command is available. If PowerShell prevents activation, use `.\.venv\Scripts\python.exe` in place of `python` without activating the environment.

## Run the sample pipeline

From the repository root, prepare the inputs on Windows:

```powershell
New-Item -ItemType Directory -Force input | Out-Null
Copy-Item sample_data/*.csv input/
python -m src.main
```

On macOS/Linux:

```sh
mkdir -p input
cp sample_data/*.csv input/
python -m src.main
```

Run the module command from the repository root. Runtime folders are located in that root, using paths derived from the source file rather than a machine-specific absolute path. No command-line configuration or package installation for the project itself is needed.

Only top-level CSV files are considered. JSON, ZIP, gzip, and subdirectories are outside the pipeline's scope. CSV filenames must be exactly `transactions_YYYYMMDD.csv`, with a real calendar date and lowercase `.csv` suffix; other CSV filenames are quarantined rather than silently skipped.

## Input schema and validation

The header must contain exactly these four unique column names, in any order:

| Column | Rule | Normalization |
| --- | --- | --- |
| `transaction_id` | Positive integer containing digits only | Converted to integer |
| `customer_name` | Non-empty text | Outer whitespace removed |
| `amount` | Digits with an optional decimal point; finite, non-negative, at most two decimal places | Written with two decimal places |
| `status` | Approved, Pending, or Declined, case-insensitive | Capitalized |

All fields are required. Extra or missing row values are rejected. UTF-8 files with or without a byte-order mark are accepted. Names remain free-form text; IDs are not deduplicated. These are demonstration business rules, not a universal transaction schema.

Example normalization:

```csv
transaction_id,customer_name,amount,status
1004,  Maria Garcia  ,850.00,approved
```

becomes:

```csv
transaction_id,customer_name,amount,status
1004,Maria Garcia,850.00,Approved
```

The two sample files produce **10 accepted and 5 rejected records**, plus two unchanged archived source files. Logs include:

```text
INFO: transactions_20260928.csv: accepted=8 rejected=0; archived
INFO: transactions_20260929.csv: accepted=2 rejected=5; archived
INFO: Batch complete: files=2 failed=0
```

Rejected-row CSVs add `extra_fields` and `error_reason` columns and preserve the original field values. For example, `ABC` as an ID receives `transaction_id must be a positive integer`. Whole-file rejection reasons are logged; the original file is moved unchanged to `error` with a `_failed.csv` suffix.

Exit code `0` means no file-level failures, including when the input folder is empty or individual records are rejected. Exit code `1` means at least one file was rejected or an I/O operation failed. Other files in the batch continue processing.

A second run sees no consumed inputs. Copying the samples into input again creates another batch; this is intentionally not duplicate detection.

## Tests and learning examples

```sh
python -m pytest
python examples/file_format.py
python examples/file_operations.py
python -m pytest examples/pytest_basics.py
```

Other lessons cover file handles, filesystem operations, paths, and basic error handling. Imports do not execute demonstrations. Examples use temporary working directories; printed file locations are temporary, and generated files disappear when the lesson finishes.

## Scope and limitations

This is a single-process local batch exercise, not a production orchestration system. It reads each file into memory, so it is intended for small demonstration datasets. It does not deduplicate transaction IDs, schedule runs, load a database, or support concurrent workers. Amounts use `float`, as in the original training, so this is not intended for precise financial arithmetic or very large monetary values. Standard file operations are not a transactional system: an interrupted process or failed cleanup can require manual inspection before retrying. During ordinary write/archive failures, created outputs are removed and the input is retained.

CSV output preserves supplied text; review untrusted data before opening it in spreadsheet software, which may interpret values as formulas. Do not put real customer data, credentials, or private files into committed sample folders. Before publishing, verify the included names and transactions are synthetic and safe to share.
