![img](https://i.imgur.com/JooOQVK.png)

# Notion Export Assistant

Notion Export Assistant is a Python-based utility designed to streamline and clean up your Notion export data. When exporting your Notion workspace, filenames and directory names often include MD5 hashes appended to ensure uniqueness. This script removes those hashes from filenames, directory names, and within the contents of Markdown (.md) files, ensuring a cleaner and more readable file structure.

⚠️ *Disclaimer* ⚠️: Use this script at your own risk. While it includes safety features like backup creation and dry run mode, always ensure you have comprehensive backups of your data before performing bulk modifications.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Safety Features](#safety-features)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features
- Remove MD5 Hashes: Cleans MD5 hashes from filenames and directory names
- Clean Markdown Content: Removes MD5 hashes embedded within Markdown links without disrupting formatting or newlines
- Preserve URL Encoding: Maintains URL-encoded separators (e.g., %20 for spaces) while removing hashes
- Backup Creation: Optionally creates backups of files before modification
- Dry Run Mode: Preview changes without applying them
- Extensible: Easily add support for additional file types or patterns as needed

## Prerequisites
- Python 3.6 or higher: Ensure you have Python installed on your system. You can download it from the official website.

## Installation

1. Clone the Repository:
```bash
git clone https://github.com/yourusername/Notion-Export-Assistant.git
```

2. Navigate to the Directory:
```bash
cd Notion-Export-Assistant
```

3. (Optional) Create a Virtual Environment:
It's recommended to run the script within a virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

4. Install Dependencies:
This script uses only standard Python libraries, so no additional installations are required. However, if you plan to extend its functionality, you might need to install additional packages.

## Usage

The script is designed to be run from the command line. It accepts the path to your exported Notion directory and provides options for dry runs and backups.

### Command-Line Arguments
- `root_dir` (required): Path to the exported Notion directory
- `--dry-run` (optional): Perform a dry run without making any changes. Useful for previewing what the script will do
- `--backup` (optional): Create .bak backup files before modifying any files. Ensures you can restore original content if needed

### Running the Script
```bash
python3 clean_notion_export.py /path/to/notion_export [--dry-run] [--backup]
```

### Example Commands

1. Basic Usage:
Remove MD5 hashes from filenames, directory names, and Markdown file contents.
```bash
python3 clean_notion_export.py /Users/yourusername/NotionExports/MyWorkspace
```

2. Dry Run Mode:
Preview the changes without applying them.
```bash
python3 clean_notion_export.py /Users/yourusername/NotionExports/MyWorkspace --dry-run
```

3. With Backup:
Create backup copies of files before modification.
```bash
python3 clean_notion_export.py /Users/yourusername/NotionExports/MyWorkspace --backup
```

4. Combined Dry Run and Backup:
Preview changes and create backups (no changes will be made).
```bash
python3 clean_notion_export.py /Users/yourusername/NotionExports/MyWorkspace --dry-run --backup
```

## Example

Before Running the Script:
```markdown
# Cheat Sheets

[Misc](Cheat%20Sheets%202d8d27defe864833a2f2481d9848be84/Misc%20172d96806c47808a8c66ffa1012f3de7.md)

# Bug Bounty / Web Pentesting

[Web Penetration Testing Reconnaissance Cheat Sheet](Cheat%20Sheets%202d8d27defe864833a2f2481d9848be84/Web%20Penetration%20Testing%20Reconnaissance%20Cheat%20Sheet%20166d96806c47809580bed05be092ba6e.md)
```

After Running the Script:
```markdown
# Cheat Sheets

[Misc](Cheat%20Sheets/Misc.md)

# Bug Bounty / Web Pentesting

[Web Penetration Testing Reconnaissance Cheat Sheet](Cheat%20Sheets/Web%20Penetration%20Testing%20Reconnaissance%20Cheat%20Sheet.md)
```

## Safety Features

### Backup Option (--backup)
Before modifying any files, the script can create a backup with a .bak extension. This ensures you can restore the original files if needed.
```bash
python3 clean_notion_export.py /path/to/notion_export --backup
```

### Dry Run Mode (--dry-run)
Allows you to see what changes will be made without actually applying them. This is useful for verifying the script's behavior before making any modifications.
```bash
python3 clean_notion_export.py /path/to/notion_export --dry-run
```

**Important**: Always ensure you have backups of your data before running scripts that modify files, even if the script includes safety features.

## Customization

The script is designed to be easily customizable. Here are some ways you can adapt it to your needs:

1. Adding Support for More File Types:
By default, the script processes the following file extensions:
```python
TEXT_FILE_EXTENSIONS = {'.md', '.markdown', '.txt', '.html', '.htm', '.json', '.csv', '.xml'}
```

To add more file types, simply include their extensions in the set:
```python
TEXT_FILE_EXTENSIONS = {'.md', '.markdown', '.txt', '.html', '.htm', '.json', '.csv', '.xml', '.rst', '.cfg'}
```

2. Modifying Regex Patterns:
If your exported files contain different patterns or additional types of hashes, you can adjust the regex patterns in the script accordingly.

3. Logging Enhancements:
For larger projects, consider modifying the script to log actions to a file for easier tracking and debugging.

## Contributing

Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

1. Fork the Repository
2. Create a Feature Branch
```bash
git checkout -b feature/YourFeatureName
```

3. Commit Your Changes
```bash
git commit -m "Add some feature"
```

4. Push to the Branch
```bash
git push origin feature/YourFeatureName
```

5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.


If you encounter any issues or need further assistance, feel free to reach out!

Happy Organizing! 📝✨
