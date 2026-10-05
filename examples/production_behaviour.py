from pathlib import Path
import logging
import shutil
import tempfile


def demonstrate():
    # ==================================================
    # Validate Input File
    # ==================================================
    print("--> Validate Input File")


    input_file = Path("input") / "transactions.csv"

    if input_file.exists() and input_file.is_file():
        print(f"Ready to process: {input_file}")
    else:
        print(f"Input file not found: {input_file}")

        # ==================================================
    # Handle File Processing Errors
    # ==================================================
    print("--> Handle File Processing Errors")

    input_file = Path("input") / "transactions.csv"

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())

    except FileNotFoundError:
        print(f"File not found: {input_file}")

    except PermissionError:
        print(f"Permission denied: {input_file}")

    except OSError as error:
        print(f"Unexpected error: {error}")

    # ==================================================
    # Logging
    # ==================================================
    print("--> Logging")


    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Starting file processing.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")

    # ==================================================
    # Archive and Error Folders
    # ==================================================
    print("--> Archive and Error Folders")

    base_path = Path.cwd()

    input_folder = base_path / "input"
    archive_folder = base_path / "archive"
    error_folder = base_path / "error"

    archive_folder.mkdir(exist_ok=True)
    error_folder.mkdir(exist_ok=True)

    print(f"Input folder:   {input_folder}")
    print(f"Archive folder: {archive_folder}")
    print(f"Error folder:   {error_folder}")

    # ==================================================
    # Move Successful File to Archive
    # ==================================================
    print("--> Move Successful File to Archive")


    base_path = Path.cwd()

    input_file = base_path / "input" / "transactions.csv"
    archive_folder = base_path / "archive"

    archive_folder.mkdir(exist_ok=True)

    if input_file.exists():
        archive_file = archive_folder / input_file.name

        shutil.move(input_file, archive_file)

        print("Moved successfully:")
        print(f"    From: {input_file}")
        print(f"    To:   {archive_file}")
    else:
        print(f"Input file does not exist: {input_file}")

    # ==================================================
    # Move Failed File to Error
    # ==================================================
    print("--> Move Failed File to Error")

    base_path = Path.cwd()

    input_file = base_path / "input" / "transactions.csv"
    error_folder = base_path / "error"

    error_folder.mkdir(exist_ok=True)

    if input_file.exists():
        error_file = error_folder / input_file.name

        shutil.move(input_file, error_file)

        print("Moved failed file:")
        print(f"    From: {input_file}")
        print(f"    To:   {error_file}")
    else:
        print(f"Input file does not exist: {input_file}")

    # ==================================================
    # Process File with Success / Failure Routing
    # ==================================================
    print("--> Process File with Success / Failure Routing")

    base_path = Path.cwd()

    input_file = base_path / "input" / "transactions.csv"
    archive_folder = base_path / "archive"
    error_folder = base_path / "error"

    archive_folder.mkdir(exist_ok=True)
    error_folder.mkdir(exist_ok=True)

    if input_file.exists():

        try:
            with open(input_file, "r", encoding="utf-8") as file:
                for line in file:
                    print(line.strip())

            archive_file = archive_folder / input_file.name
            shutil.move(input_file, archive_file)

            print(f"Processing succeeded. File moved to: {archive_file}")

        except OSError as error:
            print(f"Processing failed: {error}")

            error_file = error_folder / input_file.name
            shutil.move(input_file, error_file)

            print(f"File moved to error folder: {error_file}")

    else:
        print(f"Input file does not exist: {input_file}")

    # ==================================================
    # Processing Status and Counts
    # ==================================================
    print("--> Processing Status and Counts")

    input_file = Path("input") / "transactions.csv"

    processed_count = 0
    error_count = 0
    status = "Not Started"

    try:
        status = "Processing"

        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    # Pretend this is where record processing happens
                    print(line.strip())

                    processed_count += 1

                except OSError:
                    error_count += 1

        status = "Completed"

    except OSError as error:
        status = "Failed"
        print(f"File processing failed: {error}")

    print(f"Status: {status}")
    print(f"Records processed: {processed_count}")
    print(f"Record errors: {error_count}")


def main():
    """Run the lesson in a disposable directory, leaving repository data intact."""
    import os
    import shutil

    original_directory = Path.cwd()
    data_directory = Path(__file__).resolve().parent / "data"
    with tempfile.TemporaryDirectory() as directory:
        for filename in ("sample.txt", "transactions.csv", "transactions.json"):
            shutil.copyfile(data_directory / filename, Path(directory) / filename)
        input_directory = Path(directory) / "input"
        input_directory.mkdir()
        shutil.copyfile(data_directory / "transactions.csv", input_directory / "transactions.csv")
        try:
            os.chdir(directory)
            demonstrate()
        finally:
            os.chdir(original_directory)


if __name__ == "__main__":
    main()
