'''
⚠️ Disclaimer ⚠️: Use this script at your own risk. While it includes safety features like backup creation and dry run mode, always ensure you have comprehensive backups of your data before performing bulk modifications.
'''

import os
import re
import sys
import argparse
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_md5_from_name(name):
    """
    Remove MD5 hash from a filename or directory name.
    Assumes the hash is separated by '%20', space, hyphen, or underscore from the main name.
    """
    # Regex to match ' %20<32 hex chars>', ' <32 hex chars>', '-<32 hex chars>', '_<32 hex chars>' at the end
    pattern = re.compile(r"^(.*?)(?:%20|\s|[-_])[a-fA-F0-9]{32}(\.[^.]+)?$")
    match = pattern.match(name)
    if match:
        base = match.group(1)
        extension = match.group(2) if match.group(2) else ''
        new_name = base + extension
        return new_name
    return name

def clean_file_content(file_path, dry_run=False, backup=False):
    """
    Remove all MD5 hashes from the file content, especially within Markdown links.
    Preserves newlines and overall formatting.
    """
    # Define the file extensions to process
    TEXT_FILE_EXTENSIONS = {'.md', '.markdown', '.txt', '.html', '.htm', '.json', '.csv', '.xml'}

    # Skip files that are likely binary or not of interest
    if Path(file_path).suffix.lower() not in TEXT_FILE_EXTENSIONS:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try reading with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Skipping binary or unreadable file: {file_path} ({e})")
            return
    except PermissionError as e:
        print(f"Permission denied for file: {file_path} ({e})")
        return

    original_content = content  # Keep for comparison

    # Pattern to remove MD5 hashes preceded by '%20', space, hyphen, or underscore
    # Ensures that the hash is followed by a slash '/' or a file extension like '.md'
    hash_pattern = re.compile(r'(%20|\s|[-_])[a-fA-F0-9]{32}(?=\/|\.md)')

    def replace_hash(match):
        sep = match.group(1)
        if sep == '%20':
            # Remove the '%20' and the hash by replacing with nothing
            return ''
        else:
            # Replace ' <hash>' with ' ', '-<hash>' with '-', '_<hash>' with '_'
            return sep

    # Apply the substitution using the replacement function
    new_content, num_subs = hash_pattern.subn(replace_hash, content)

    # No additional cleanup steps to avoid altering newlines and formatting

    if num_subs > 0:
        if backup and not dry_run:
            backup_path = f"{file_path}.bak"
            try:
                shutil.copy2(file_path, backup_path)
                print(f"Backup created: {backup_path}")
            except Exception as e:
                print(f"Error creating backup for '{file_path}': {e}")
                return

        if not dry_run:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Cleaned {num_subs} hashes in file: {file_path}")
            except Exception as e:
                print(f"Error writing to file '{file_path}': {e}")
        else:
            print(f"[Dry Run] Would clean {num_subs} hashes in file: {file_path}")

def rename_entities(root_dir, dry_run=False):
    """
    Recursively rename directories and files by removing MD5 hashes.
    """
    # Walk the directory tree from bottom up to handle nested directories
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Rename files
        for filename in filenames:
            new_filename = remove_md5_from_name(filename)
            if new_filename != filename:
                src = os.path.join(dirpath, filename)
                dst = os.path.join(dirpath, new_filename)
                if dry_run:
                    print(f"[Dry Run] Would rename file: '{src}' -> '{dst}'")
                else:
                    try:
                        os.rename(src, dst)
                        print(f"Renamed file: '{src}' -> '{dst}'")
                    except Exception as e:
                        print(f"Error renaming file '{src}': {e}")

        # Rename directories
        for dirname in dirnames:
            new_dirname = remove_md5_from_name(dirname)
            if new_dirname != dirname:
                src = os.path.join(dirpath, dirname)
                dst = os.path.join(dirpath, new_dirname)
                if dry_run:
                    print(f"[Dry Run] Would rename directory: '{src}' -> '{dst}'")
                else:
                    try:
                        os.rename(src, dst)
                        print(f"Renamed directory: '{src}' -> '{dst}'")
                    except Exception as e:
                        print(f"Error renaming directory '{src}': {e}")

def clean_contents(root_dir, dry_run=False, backup=False):
    """
    Recursively clean file contents by removing MD5 hashes.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            clean_file_content(file_path, dry_run=dry_run, backup=backup)

def select_folder_via_dialog():
    """
    Opens a GUI dialog for folder selection and returns the selected path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.update()  # Prevents the window from appearing briefly
    folder_selected = filedialog.askdirectory(title="Select Root Directory")
    root.destroy()
    return folder_selected

def main():
    parser = argparse.ArgumentParser(
        description="Clean Notion Export MD5 Hashes from Filenames, Directory Names, and File Contents"
    )
    parser.add_argument(
        "root_dir",
        nargs='?',
        help="Path to the exported Notion directory. If not provided, a folder selection dialog will appear."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making changes"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backups of files before modifying them"
    )
    args = parser.parse_args()

    # Determine the root directory
    if args.root_dir:
        root_dir = args.root_dir
    else:
        root_dir = select_folder_via_dialog()
        if not root_dir:
            print("No directory selected. Exiting.")
            sys.exit(1)

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"Selected directory: {root_dir}")
    print(f"Dry Run: {'Enabled' if args.dry_run else 'Disabled'}")
    print(f"Backup: {'Enabled' if args.backup else 'Disabled'}\n")

    print("Starting renaming of files and directories...")
    rename_entities(root_dir, dry_run=args.dry_run)

    print("\nStarting cleaning of file contents...")
    clean_contents(root_dir, dry_run=args.dry_run, backup=args.backup)

    if not args.dry_run:
        print("\nMD5 hash removal completed successfully.")
    else:
        print("\nDry run completed. No changes were made.")

if __name__ == "__main__":
    main()
