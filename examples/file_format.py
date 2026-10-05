import csv
from pathlib import Path
import json
from io import StringIO
import gzip
import zipfile
import tempfile


def demonstrate():


    # ==================================================
    # Reading CSV Files
    # ==================================================
    print("--> Reading CSV Files")

    file_path = Path("transactions.csv")

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            print(row)

    # ==================================================
    # Reading CSV Files with DictReader
    # ==================================================
    print("--> Reading CSV Files with DictReader")

    file_path = Path("transactions.csv")

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            print(row)

    # ==================================================
    # Writing CSV Files
    # ==================================================
    print("--> Writing CSV Files")

    file_path = Path("output_transactions.csv")

    rows = [
        ["transaction_id", "customer_name", "amount", "status"],
        [2001, "James Smith", 95.50, "Approved"],
        [2002, "Mary Jones", 140.00, "Pending"],
        [2003, "David Brown", 75.25, "Declined"]
    ]

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        for row in rows:
            writer.writerow(row)

    print(f"CSV created: {file_path}")

    # ==================================================
    # Writing CSV Files with DictWriter
    # ==================================================
    print("--> Writing CSV Files with DictWriter")

    file_path = Path("output_transactions_dict.csv")

    fieldnames = [
        "transaction_id",
        "customer_name",
        "amount",
        "status"
    ]

    rows = [
        {
            "transaction_id": 3001,
            "customer_name": "John Smith",
            "amount": 125.50,
            "status": "Approved"
        },
        {
            "transaction_id": 3002,
            "customer_name": "Lisa Green",
            "amount": 89.25,
            "status": "Pending"
        },
        {
            "transaction_id": 3003,
            "customer_name": "Mark White",
            "amount": 200.00,
            "status": "Approved"
        }
    ]

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    print(f"CSV created: {file_path}")

    # ==================================================
    # Reading JSON Files
    # ==================================================
    print("--> Reading JSON Files")


    file_path = Path("transactions.json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(data)
    print(type(data))

    # ==================================================
    # Writing JSON Files
    # ==================================================
    print("--> Writing JSON Files")

    file_path = Path("output_transactions.json")

    transactions = [
        {
            "transaction_id": 2001,
            "customer_name": "James Smith",
            "amount": 95.50,
            "status": "Approved"
        },
        {
            "transaction_id": 2002,
            "customer_name": "Mary Jones",
            "amount": 140.00,
            "status": "Pending"
        }
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)

    print(f"JSON created: {file_path}")

    transaction = {
        "transaction_id": 1001,
        "customer_name": "Bob Smith",
        "amount": 75.50,
        "approved": True
    }

    # ==================================================
    # dumps() - Python object to JSON string
    # ==================================================

    json_string = json.dumps(transaction, indent=4)

    print(json_string)
    print(type(json_string))

    # ==================================================
    # loads() - JSON string to Python object
    # ==================================================

    python_object = json.loads(json_string)

    print(python_object)
    print(type(python_object))

    # ==================================================
    # In-Memory Text Files with StringIO
    # ==================================================
    print("--> In-Memory Text Files with StringIO")


    text_data = """transaction_id,customer_name,amount
    1001,Bob Smith,75.50
    1002,Alice Jones,120.00
    """

    memory_file = StringIO(text_data)

    for line in memory_file:
        print(line.strip())

    # ==================================================
    # Reading and Writing gzip Files
    # ==================================================
    print("--> Reading and Writing gzip Files")


    file_path = Path("transactions.txt.gz")

    with gzip.open(file_path, "wt", encoding="utf-8") as file:
        file.write("1001,Bob Smith,75.50\n")
        file.write("1002,Alice Jones,120.00\n")

    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        for line in file:
            print(line.strip())

    # ==================================================
    # ZIP Files
    # ==================================================
    print("--> ZIP Files")


    zip_path = Path("transactions.zip")

    with zipfile.ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "transactions.csv",
            "transaction_id,customer_name,amount\n"
            "1001,Bob Smith,75.50\n"
            "1002,Alice Jones,120.00\n"
        )

    print(f"ZIP created: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        with zip_file.open("transactions.csv") as file:
            contents = file.read().decode("utf-8") #default is bytes so need to decode it to return string

    print(contents)


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
