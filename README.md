# file-integrity-checker
A Python-based tool to monitor file changes using SHA-256 hashing. Detects modified, deleted, and newly added files in a directory to ensure data integrity.

# 🔒 File Integrity Checker

This is a simple Python-based tool that monitors and detects changes in files within a specified directory. It helps ensure data integrity by tracking file modifications, deletions, or additions using cryptographic hash values and content comparison.

## 📂 Project Structure

📁 your-project-folder/
│
├── Fileintegritychecker.py # Main Python script
├── file_baseline.json # Stores original file hashes
├── file_contents.json # Stores original file contents
└── testfile/ # Directory containing files to monitor

## 🚀 Features

- Calculates SHA-256 hashes for all files in a given directory.
- Compares current hashes with the saved baseline to detect changes.
- Highlights added and deleted lines in modified text files.
- Detects and lists newly added or deleted files.
- Easy-to-use CLI interface.

## ⚙️ How It Works

1. **Create Baseline**:
   - Stores the current state of all files (hashes + contents).
2. **Check Integrity**:
   - Compares the current file state with the baseline and highlights differences.

## 🛠️ Usage

### Step 1: Setup

Make sure you have Python installed (preferably Python 3.6+).

Clone or download the repository and navigate into it:

git clone https://github.com/soham3625/file-integrity-checker.git
cd file-integrity-checker

### Step 2: Run the Script
python Fileintegritychecker.py

You will be prompted with:


🔒 File Integrity Checker
1. Create Baseline
2. Check Integrity
Enter choice (1/2):
Choose 1 to create a baseline.

Choose 2 to check for changes since the last baseline.

✅ Ensure the directory testfile/ contains the files you want to monitor.

📝 Example Output:-
🔍 Integrity Check Report
-------------------------

[MODIFIED FILE] testfile/1.txt

--- Differences Detected ---
[-] old line
[+] new line

[NEW FILES]
 - testfile/new.txt

[DELETED FILES]
 - testfile/old.txt
