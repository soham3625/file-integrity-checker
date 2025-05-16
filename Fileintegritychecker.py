import os
import hashlib
import json
import difflib

# Directory to monitor
DIRECTORY = 'testfile'
BASELINE_FILE = "file_baseline.json"
CONTENT_SNAPSHOT_FILE = "file_contents.json"

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def read_text_file(file_path):
    """Read and return text content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except:
        return []

def create_baseline(directory):
    """Create and save baseline hashes and file contents for all files in a directory."""
    baseline = {}
    contents = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            file_hash = calculate_file_hash(path)
            if file_hash:
                baseline[path] = file_hash
                contents[path] = read_text_file(path)
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)
    with open(CONTENT_SNAPSHOT_FILE, "w") as f:
        json.dump(contents, f, indent=4)
    print(f"✅ Baseline and content snapshot created and saved.")

def compare_file_changes(old_lines, new_lines):
    """Compare old and new lines and show clear additions and deletions."""
    diff = difflib.ndiff(old_lines, new_lines)
    changes = []
    for line in diff:
        if line.startswith('- '):  # Line removed
            changes.append(f"\033[91m[-] {line[2:].rstrip()}\033[0m")  # Red
        elif line.startswith('+ '):  # Line added
            changes.append(f"\033[92m[+] {line[2:].rstrip()}\033[0m")  # Green
    return changes

def check_integrity(directory):
    """Compare current file hashes with baseline and report changes."""
    if not os.path.exists(BASELINE_FILE) or not os.path.exists(CONTENT_SNAPSHOT_FILE):
        print("❌ Baseline not found. Please create it first using create_baseline().")
        return

    with open(BASELINE_FILE, "r") as f:
        old_hashes = json.load(f)

    with open(CONTENT_SNAPSHOT_FILE, "r") as f:
        old_contents = json.load(f)

    new_hashes = {}
    modified = []
    deleted = []
    new_files = []

    print("\n🔍 Integrity Check Report")
    print("-------------------------")

    # Generate current hashes
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            file_hash = calculate_file_hash(path)
            new_hashes[path] = file_hash

            if path in old_hashes:
                if old_hashes[path] != file_hash:
                    modified.append(path)
                    print(f"\n[MODIFIED FILE] {path}")
                    old_lines = old_contents.get(path, [])
                    new_lines = read_text_file(path)
                    diff = compare_file_changes(old_lines, new_lines)
                    if diff:
                        print("\n--- Differences Detected ---")
                        print("\n".join(diff))
                    else:
                        print(" - Changes not detectable (binary or unreadable file).")
            else:
                new_files.append(path)

    # Check for deleted files
    for path in old_hashes:
        if path not in new_hashes:
            deleted.append(path)

    if deleted:
        print("\n[DELETED FILES]")
        for f in deleted:
            print(" -", f)
    if new_files:
        print("\n[NEW FILES]")
        for f in new_files:
            print(" -", f)

    if not (modified or deleted or new_files):
        print("\n✅ All files are intact. No changes detected.")

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    print("🔒 File Integrity Checker")
    print("1. Create Baseline")
    print("2. Check Integrity")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        create_baseline(DIRECTORY)
    elif choice == "2":
        check_integrity(DIRECTORY)
    else:
        print("❌ Invalid choice. Exiting.")
