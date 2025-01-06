'''
Script is still WIP, the regex pattern still does not capture some instances of hashes inside of files, but should still work in most cases. Feel free to edit and adjust this script to your liking.
'''

import os
import re
import argparse

class NotionCleaner:
    def __init__(self, directory, dry_run=False):
        self.directory = directory
        self.dry_run = dry_run
        
    def clean_filename(self, filename):
        """Remove hash from filename."""
        # Pattern matches: name + space + 32 char hash + extension
        pattern = r'^(.+?)\s+[a-f0-9]{32}(\..+)$'
        match = re.match(pattern, filename)
        if match:
            return f"{match.group(1)}{match.group(2)}"
        return filename

    def encode_path(self, path):
        """Encode spaces in path with %20."""
        parts = path.split('/')
        encoded_parts = [part.replace(' ', '%20') for part in parts]
        return '/'.join(encoded_parts)

    def clean_content(self, content):
        """Clean markdown links."""
        # Find all markdown links
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Remove ** from link text and path
            clean_text = link_text.replace('**', '')
            
            # Fix duplicate parts and cleanup path
            clean_path = clean_text
            
            # Handle special cases where the title is repeated in the path
            if "Injection Cheat Sheet" in clean_path:
                clean_path = clean_path.replace(" Injection Cheat Sheet Injection Cheat Sheet", " Injection Cheat Sheet")
            if "Cheat Sheet Cheat Sheet" in clean_path:
                clean_path = clean_path.replace(" Cheat Sheet Cheat Sheet", " Cheat Sheet")
                
            # Remove hash patterns
            clean_path = re.sub(r'%20[0-9a-f]{32}\.md\)$', '', clean_path)
            clean_path = re.sub(r'\.md\)\.md\)$', '', clean_path)
            
            # Encode spaces properly
            clean_path = clean_path.replace(' ', '%20')
            
            return f'[{link_text}](Cheat%20Sheets/{clean_path}.md)'
        
        # Clean up the links
        cleaned = re.sub(pattern, replace_link, content)
        
        # Also clean any leftover ** in the headers
        cleaned = cleaned.replace('**', '')
        
        # Remove any duplicate .md extensions
        cleaned = re.sub(r'\.md\.md\)', '.md)', cleaned)
        
        return cleaned

    def clean_directory_name(self, dirname):
        """Remove hash from directory name."""
        pattern = r'^(.+?)\s+[a-f0-9]{32}$'
        match = re.match(pattern, dirname)
        if match:
            return match.group(1)
        return dirname

    def process_file(self, filepath):
        """Process markdown file content."""
        if not filepath.lower().endswith('.md'):
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = self.clean_content(content)
            
            if new_content != content and not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated content in: {filepath}")
            elif new_content != content:
                print(f"Would update content in: {filepath}")
                
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

    def rename_file(self, old_path):
        """Rename file to remove hash."""
        directory = os.path.dirname(old_path)
        filename = os.path.basename(old_path)
        new_filename = self.clean_filename(filename)
        
        if new_filename != filename:
            new_path = os.path.join(directory, new_filename)
            if self.dry_run:
                print(f"Would rename: {old_path} -> {new_path}")
                return old_path
                
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")
                return new_path
            except Exception as e:
                print(f"Error renaming {old_path}: {e}")
                return old_path
        return old_path

    def rename_directory(self, old_path):
        """Rename directory to remove hash."""
        parent_dir = os.path.dirname(old_path)
        dirname = os.path.basename(old_path)
        new_dirname = self.clean_directory_name(dirname)
        
        if new_dirname != dirname:
            new_path = os.path.join(parent_dir, new_dirname)
            if self.dry_run:
                print(f"Would rename directory: {old_path} -> {new_path}")
                return old_path
                
            try:
                os.rename(old_path, new_path)
                print(f"Renamed directory: {old_path} -> {new_path}")
                return new_path
            except Exception as e:
                print(f"Error renaming directory {old_path}: {e}")
                return old_path
        return old_path

    def process_directory(self):
        """Process all files and directories recursively."""
        print(f"\nProcessing directory: {self.directory}")
        print("Dry run mode:", "Yes" if self.dry_run else "No")
        
        # First, clean directory names (bottom-up to handle nested directories)
        for root, dirs, _ in os.walk(self.directory, topdown=False):
            for dirname in dirs:
                old_dir_path = os.path.join(root, dirname)
                self.rename_directory(old_dir_path)

        # Then process files
        for root, _, files in os.walk(self.directory):
            for filename in files:
                if filename.endswith('.md'):
                    filepath = os.path.join(root, filename)
                    # First process content
                    self.process_file(filepath)
                    # Then rename file
                    self.rename_file(filepath)

def main():
    parser = argparse.ArgumentParser(
        description="Clean up Notion markdown exports by removing hashes and fixing links."
    )
    parser.add_argument(
        "directory",
        help="Directory containing the Notion export files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory")
        return 1
        
    cleaner = NotionCleaner(args.directory, args.dry_run)
    cleaner.process_directory()
    
    print("\nProcessing complete!")
    return 0

if __name__ == "__main__":
    exit(main())