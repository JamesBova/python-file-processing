from pathlib import Path
import os
import tempfile


def demonstrate():
    # ==================================================
    # Absolute and Relative Paths
    # ==================================================
    print("--> Absolute and Relative Paths")


    current_path = Path.cwd()

    absolute_path = current_path / "input" / "transactions.csv"
    relative_path = Path("input") / "transactions.csv"

    print(f"Absolute path: {absolute_path}")
    print(f"Relative path: {relative_path}")

    # ==================================================
    # Resolving Relative Paths
    # ==================================================
    print("--> Resolving Relative Paths")

    relative_path = Path("input") / "transactions.csv"

    resolved_path = relative_path.resolve()

    print(f"Relative path: {relative_path}")
    print(f"Resolved path: {resolved_path}")

    # ==================================================
    # Parent Directories
    # ==================================================
    print("--> Parent Directories")

    file_path = Path("input") / "archive" / "transactions.csv"

    print(f"Full path: {file_path}")
    print(f"Parent: {file_path.parent}")
    print(f"Parent's parent: {file_path.parent.parent}")

    # ==================================================
    # Filename, Stem, and Suffix
    # ==================================================
    print("--> Filename, Stem, and Suffix")

    file_path = Path("input") / "transactions_20260927.csv"

    print(f"Full path: {file_path}")
    print(f"File name: {file_path.name}")
    print(f"Stem: {file_path.stem}")
    print(f"Suffix: {file_path.suffix}")

    json_path = file_path.with_suffix(".json")

    print(f"Original: {file_path}")
    print(f"Changed:  {json_path}")

    # ==================================================
    # Changing a File Name
    # ==================================================
    print("--> Changing a File Name")

    file_path = Path("input") / "transactions_20260927.csv"

    new_file_path = file_path.with_name("transactions_latest.csv")

    print(f"Original: {file_path}")
    print(f"Changed:  {new_file_path}")

    # ==================================================
    # Absolute vs Relative Check
    # ==================================================
    print("--> Absolute vs Relative Check")

    relative_path = Path("input") / "transactions.csv"
    absolute_path = Path.cwd() / "input" / "transactions.csv"

    print(f"Relative path: {relative_path}")
    print(f"Is absolute? {relative_path.is_absolute()}")

    print(f"Absolute path: {absolute_path}")
    print(f"Is absolute? {absolute_path.is_absolute()}")

    # ==================================================
    # Path Parts
    # ==================================================
    print("--> Path Parts")

    file_path = Path("input") / "archive" / "transactions_20260927.csv"

    print(f"Full path: {file_path}")
    print(f"Parts: {file_path.parts}")

    for part in file_path.parts:
        print(part)

    # ==================================================
    # Resolving . and ..
    # ==================================================
    print("--> Resolving . and ..")

    path_with_navigation = Path("input") / ".." / "output" / "." / "results.csv"

    #go into input
    #.. = go back up
    #go into output
    #. = stay where you are
    #then results.csv

    print(f"Original path: {path_with_navigation}")
    print(f"Resolved path: {path_with_navigation.resolve()}")

    # ==================================================
    # pathlib vs os.path
    # ==================================================
    print("--> pathlib vs os.path")


    pathlib_path = Path("input") / "transactions.csv"
    os_path = os.path.join("input", "transactions.csv")

    print(f"pathlib: {pathlib_path}")
    print(f"os.path: {os_path}")

    # Build a path
    Path("input") / "transactions.csv"
    os.path.join("input", "transactions.csv")



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
