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
```

2. Make the script executable (Unix-based systems):
```bash
chmod +x notion_cleaner.py
```

## Usage

Basic usage:
```bash
python notion_cleaner.py /path/to/notion/export
```

Preview changes without making them (dry run):
```bash
python notion_cleaner.py /path/to/notion/export --dry-run
```

## Examples

### File Renaming
Before:
```
Misc 172d96806c47808a8c66ffa1012f3de7.md
```
After:
```
Misc.md
```

### Directory Renaming
Before:
```
Cheat Sheets 2d8d27defe864833a2f2481d9848be84/
```
After:
```
Cheat Sheets/
```

### Markdown Link Cleaning
Before:
```markdown
[**XXE (XML External Entity) Injection Cheat Sheet**](Cheat%20Sheets/XXE%20(XML%20External%20Entity)%20Injection%20Cheat%20Sheet.md)%20Cheat%20Sheet%2014dd96806c478045921ee4ea505b192e.md)
```
After:
```markdown
[XXE (XML External Entity) Injection Cheat Sheet](Cheat%20Sheets/XXE%20(XML%20External%20Entity)%20Injection%20Cheat%20Sheet.md)
```

## Backup Warning

⚠️ It's recommended to backup your files before running this script, as it makes irreversible changes to file names and content.

## Known Limitations

- Only processes text-based files for content cleaning (.md and .html)
- Only renames files with the supported extensions
- Assumes Notion's standard export format and hash patterns

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use and modify for your own purposes.
