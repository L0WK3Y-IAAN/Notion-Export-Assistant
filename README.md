# Notion Export File Cleaner

A Python script to clean up Notion exported files by removing hashes, fixing file names, and correcting markdown links.

## Description

When exporting from Notion, files and directories often contain extra elements like:
- 32-character hashes in filenames and directory names
- Spaces before file extensions
- Encoded spaces (%20) in paths
- Duplicate markdown link text
- Bold markers (**) in markdown links

This script cleans up these artifacts to create a more manageable file structure.

## Features

- Removes 32-character hashes from filenames and directory names
- Removes spaces before file extensions (.md, .html, .pdf, .csv)
- Properly encodes spaces in markdown links
- Removes duplicate text and hashes from markdown links
- Supports dry run mode to preview changes
- Handles nested directories
- Processes multiple file types (.md, .html, .pdf, .csv)

## Requirements

- Python 3.6+
- No additional dependencies required

## Installation

1. Clone this repository or download the script:
```bash
git clone <repository-url>
