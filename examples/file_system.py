import os
import glob
import shutil
import tempfile
from pathlib import Path
import tempfile


def demonstrate():
    # ==================================================
    # Current Working Directory
    # ==================================================
    print("--> Current Working Directory")


    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")

    # ==================================================
    # Listing Files and Folders
    # ==================================================
    print("--> Listing Files and Folders")

    items = os.listdir(current_directory)

    for item in items:
        print(item)

    # ==================================================
    # Creating Directories
    # ==================================================
    print("--> Creating Directories")

    new_directory = os.path.join(current_directory, "test_folder")

    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
        print(f"Created directory: {new_directory}")
    else:
        print(f"Directory already exists: {new_directory}")

    # ==================================================
    # Checking Whether Files or Folders Exist
    # ==================================================
    print("--> Checking Whether Files or Folders Exist")

    test_path = os.path.join(current_directory, "test_folder")

    if os.path.isdir(test_path):
        print("This path is a directory.")
    if os.path.isfile(test_path):
        print("This path is a file.")

    # ==================================================
    # Renaming Files and Folders
    # ==================================================
    print("--> Renaming Files and Folders")

    old_name = os.path.join(current_directory, "test_folder")
    new_name = os.path.join(current_directory, "renamed_test_folder")

    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print("Renamed:")
        print(f"    From: {old_name}")
        print(f"    To:   {new_name}")
    else:
        print(f"Path does not exist: {old_name}")

    # ==================================================
    # Removing Files and Directories
    # ==================================================
    print("--> Removing Files and Directories")

    directory_to_remove = os.path.join(current_directory, "renamed_test_folder")

    if os.path.exists(directory_to_remove):
        os.rmdir(directory_to_remove) #only will remove if nothing inside. os.remove(file_path) for removing file
        print(f"Removed directory: {directory_to_remove}")
    else:
        print(f"Directory does not exist: {directory_to_remove}")

    # ==================================================
    # Finding Files with glob
    # ==================================================
    print("--> Finding Files with glob")

    search_pattern = os.path.join(current_directory, "*.py")

    python_files = glob.glob(search_pattern)

    for file in python_files:
        print(file)


    # ==================================================
    # Copying and Moving Files with shutil
    # ==================================================
    print("--> Copying and Moving Files with shutil")

    source_file = os.path.join(current_directory, "sample.txt")
    copied_file = os.path.join(current_directory, "sample_copy.txt")
    moved_file = os.path.join(current_directory, "sample_moved.txt")

    with open(source_file, "w", encoding="utf-8") as file:
        file.write("This is a test file.")

    shutil.copy(source_file, copied_file)

    print("Copied file:")
    print(f"    From: {source_file}")
    print(f"    To:   {copied_file}")

    shutil.move(copied_file, moved_file)

    print("Moved file:")
    print(f"    From: {copied_file}")
    print(f"    To:   {moved_file}")

    # ==================================================
    # Temporary Files
    # ==================================================
    print("--> Temporary Files")


    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as temp_file:
        temp_file.write("Temporary data")
        print(f"Temporary file created: {temp_file.name}")

    # ==================================================
    # Temporary Directories
    # ==================================================
    print("--> Temporary Directories")

    with tempfile.TemporaryDirectory() as temp_directory:
        print(f"Temporary directory: {temp_directory}")

    # ==================================================
    # pathlib Basics
    # ==================================================
    print("--> pathlib Basics")

    current_path = Path.cwd()

    print(f"Current path: {current_path}")
    print(type(current_path))
    test_file = current_path / "sample.txt"

    print(test_file)
    print(test_file.exists())
    print(test_file.is_file())
    print(test_file.is_dir())

    print(test_file.name)
    print(test_file.stem)
    print(test_file.suffix)
    print(test_file.parent)


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
