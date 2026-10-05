"""Run the transaction CSV pipeline from the repository root."""

import logging
from pathlib import Path

from src.file_processor import process_directory


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    data_dir = Path(__file__).resolve().parent.parent
    try:
        return 1 if process_directory(data_dir) else 0
    except OSError as error:
        logging.error("Cannot access data directories: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
