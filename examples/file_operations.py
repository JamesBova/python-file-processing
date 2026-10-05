from pathlib import Path
import tempfile


def demonstrate():
    # ==================================================
    # Writing a File
    # ==================================================
    print("--> Writing a File")


    file_path = Path("sample.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("This is my first file-processing example.")

    print(f"File created: {file_path}")

    # ==================================================
    # Reading an Entire File
    # ==================================================
    print("--> Reading an Entire File")

    file_path = Path("sample.txt")

    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.read()

    print(contents)

    # ==================================================
    # Reading a File Line by Line
    # ==================================================
    print("--> Reading a File Line by Line")


    file_path = Path("sample.txt")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            print(line.strip())

    # ==================================================
    # Appending to a File
    # ==================================================
    print("--> Appending to a File")

    file_path = Path("sample.txt")

    with open(file_path, "a", encoding="utf-8") as file:
        file.write("\nThis line was appended.")

    print("Text appended.")

    # ==================================================
    # Different Ways to Read a File
    # ==================================================
    print("--> Different Ways to Read a File")

    file_path = Path("sample.txt")

    # read()
    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.read()
        print("read():")
        print(contents)

    # readline()
    with open(file_path, "r", encoding="utf-8") as file:
        first_line = file.readline()
        print("readline():")
        print(first_line.strip())

    # readlines()
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        print("readlines():")
        print(lines)

    # ==================================================
    # Read and Write Modes
    # ==================================================
    print("--> Read and Write Modes")

    file_path = Path("sample.txt")

    with open(file_path, "r+", encoding="utf-8") as file:
        contents = file.read()

        print("Current contents:")
        print(contents)

        file.write("\nAdded using r+ mode.")

        # ==================================================
    # File Position with tell() and seek()
    # ==================================================
    print("--> File Position with tell() and seek()")

    file_path = Path("sample.txt")

    with open(file_path, "r", encoding="utf-8") as file:
        print(f"Starting position: {file.tell()}")

        first_line = file.readline()
        print(f"First line: {first_line.strip()}")

        print(f"Position after readline(): {file.tell()}")

        file.seek(0)

        print(f"Position after seek(0): {file.tell()}")

        contents = file.read()
        print(contents)

    # ==================================================
    # File Encoding
    # ==================================================
    print("--> File Encoding")

    file_path = Path("encoding_example.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Hello café ☕")

    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.read()

    print(contents)

    # ==================================================
    # Binary Files
    # ==================================================
    print("--> Binary Files")

    file_path = Path("sample.txt")

    with open(file_path, "rb") as file:
        data = file.read()

    print(data)
    print(type(data))

    # ==================================================
    # Writing Multiple Lines
    # ==================================================
    print("--> Writing Multiple Lines")


    file_path = Path("multiple_lines.txt")

    lines = [
        "First line\n",
        "Second line\n",
        "Third line\n"
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

    print("Multiple lines written.")


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
