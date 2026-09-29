# ==================================================
# File Objects / File Handles
# ==================================================
print("--> File Objects / File Handles")

file = open("sample.txt", "r", encoding="utf-8")

print(file)
print(type(file))

file.close()

with open("sample.txt", "r", encoding="utf-8") as file:
    print(f"Inside with block: {file.closed}")

print(f"After with block: {file.closed}")

# ==================================================
# Streaming a File
# ==================================================
print("--> Streaming a File")

with open("sample.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())

# ==================================================
# Buffering
# ==================================================
print("--> Buffering")

with open(
    "sample.txt",
    "r",
    encoding="utf-8",
    buffering=16384
) as file:
    for line in file:
        print(line.strip())

# ==================================================
# File Position
# ==================================================
print("--> File Position")

with open("sample.txt", "r", encoding="utf-8") as file:
    print(f"Start: {file.tell()}")

    line = file.readline()
    print(f"After one line: {file.tell()}")

    file.seek(0)
    print(f"After seek(0): {file.tell()}")

# ==================================================
# Encodings
# ==================================================
print("--> Encodings")

with open("encoding_example.txt", "w", encoding="utf-8") as file:
    file.write("café")

with open("encoding_example.txt", "r", encoding="utf-8") as file:
    contents = file.read()

print(contents)

# ==================================================
# Newline Handling
# ==================================================
print("--> Newline Handling")

with open("newlines.txt", "w", encoding="utf-8") as file:
    file.write("First line\n")
    file.write("Second line\n")
    file.write("Third line\n")

with open("newlines.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(repr(line)) #repr will show hidden \n

# ==================================================
# Resource Cleanup with Exceptions
# ==================================================
print("--> Resource Cleanup with Exceptions")

try:
    with open("sample.txt", "r", encoding="utf-8") as file:
        print(f"Inside with block - closed? {file.closed}")

        # Force an error for demonstration
        number = int("not-a-number")

except ValueError:
    print("A ValueError occurred.")

print(f"After with block - closed? {file.closed}")