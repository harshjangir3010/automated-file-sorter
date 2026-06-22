# 🗂️ Automated File Sorter

A Python application that automatically organizes files
into folders based on their file type.

## Features
- Automatically detects file types
- Moves files into correct folders
- Supports custom sorting rules via rules.json
- Logs all activity to sorter.log
- Auto monitors folder for new files

## Supported File Types
| Extension | Folder |
|-----------|--------|
| .txt | TextFiles |
| .png .jpg .jpeg | Images |
| .pdf | PDFs |
| .mp3 | Music |
| .mp4 | Videos |
| .zip | ZIPs |
| .docx | WordFiles |
| .xlsx | Spreadsheets |
| .py | PythonFiles |

## How To Run

### Install required library:
pip install watchdog

### Run the sorter:
python sorter.py

## Project Structure
📁 Project/
├── sorter.py      # main program
├── rules.json     # custom sorting rules
└── sorter.log     # activity log

## Built With
- Python 3
- pathlib
- shutil
- logging
- json
- watchdog

## Author
Harsh