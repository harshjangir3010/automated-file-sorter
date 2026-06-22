from pathlib import Path        # pathlib used to build Path tool
import shutil                   # It helps us to move, copy, delete files
import logging                  # new import for logging
import json                     
import time                     # wait/sleep
from watchdog.observers import Observer             # CCTV camera 👁️
from watchdog.events import FileSystemEventHandler  # receptionist 👩

# ─────────────────────────────
# Setup the logger
# ─────────────────────────────
logging.basicConfig(
    level   = logging.DEBUG,
    format  = "%(asctime)s  -  %(levelname)s  -  %(message)s",
    handlers= [
        logging.FileHandler("sorter.log", mode="w"),  # save to file
        logging.StreamHandler()                        # show on screen
    ]
)
logger = logging.getLogger("FileSorter")

# ─────────────────────────────
# Function to load rules
# ─────────────────────────────
def load_rules(rules_files="rules.json"):
    if not Path(rules_files).exists():
        logger.warning("rules.json not found! Using default rules.")
        return {".txt": "TextFiles", ".png": "Images", ".pdf": "PDFs"}

    # read and return rules
    with open(rules_files, "r") as f:
        rules = json.load(f)
        logger.info(f"Loaded {len(rules)} rules from {rules_files}")
        return rules

# ─────────────────────────────
# Function to sort a single file
# (your old sorting code — now 
#  wrapped in a function!)
# ─────────────────────────────
def sort_file(file_path, file_types):

    file = Path(file_path)

    time.sleep(1)            # wait for file to finish copying!

    if not file.is_file():   # skip if it's a folder
        return

    extension = file.suffix  # get the extension

    if extension in file_types:

        # find the destination folder name
        folder_name = file_types[extension]

        # build the full destination folder path
        destination_folder = Path(folder_name)

        # create destination folder if it doesn't exist
        destination_folder.mkdir(exist_ok=True)

        # move the file! with try & except for error handling
        try:
            shutil.move(str(file), str(destination_folder / file.name))
            logger.info(f"Moved :    {file.name} --- {folder_name}/")

        except FileNotFoundError:
            logger.error(f"Skipped :  {file.name} --- disappeared!")

        except PermissionError:
            logger.error(f"Skipped :  {file.name} --- permission denied!")

        except shutil.Error:
            logger.warning(f"Skipped :  {file.name} --- already exists in {folder_name}/!")

        except Exception as e:
            logger.error(f"Error :    {file.name} --- something went wrong ({e})")

    else:
        logger.warning(f"Unknown :  {file.name} --- no rule for '{extension}'!")

# ─────────────────────────────
# Receptionist (Event Handler)
# ─────────────────────────────
class FileSorterHandler(FileSystemEventHandler):

    def __init__(self, file_types):
        self.file_types = file_types   # store rules in drawer!

    def on_created(self, event):       # runs when new file appears!
        if not event.is_directory:
            logger.info(f"👀 New file spotted : {Path(event.src_path).name}")
            sort_file(event.src_path, self.file_types)

# ─────────────────────────────
# Setup folders
# ─────────────────────────────
folders = ["TestSorter", "Images", "PDFs",
           "TextFiles", "ZIPs", "Music", 
           "Videos", "PythonFiles"]

for folder in folders:
    Path(folder).mkdir(exist_ok=True)

# ─────────────────────────────
# Create test files
# ─────────────────────────────
test_folder = Path("TestSorter")

(test_folder / "notes.txt").touch()
(test_folder / "photo.png").touch()
(test_folder / "harsh.pdf").touch()
(test_folder / "archive.zip").touch()
(test_folder / "song.mp3").touch()
(test_folder / "video.mp4").touch()
(test_folder / "script.py").touch()
(test_folder / "pyhton.pdf").touch()

logger.info("Test Files Created!")

# ─────────────────────────────
# Load rules from JSON file
# ─────────────────────────────
FILE_TYPES = load_rules()

# ─────────────────────────────
# Check source folder exists
# ─────────────────────────────
source_folder = Path("TestSorter")

if not source_folder.exists():
    logger.error(f"Error: '{source_folder}' is not found!")
    logger.error("Please check the folder name and try again.")

else:
    logger.info(f"Folder found : {source_folder}")

    # ─────────────────────────
    # Sort existing files FIRST
    # (files already in folder
    #  before watcher starts!)
    # ─────────────────────────
    logger.info("Sorting existing files first...")
    logger.info("-------------------------------")

    for file in test_folder.iterdir():

        # skip if it is a folder, not a file
        if file.is_dir():
            continue

        sort_file(str(file), FILE_TYPES)   # ← uses our function!

    logger.info("------------------------------------")
    logger.info("Existing files sorted!")

    # ─────────────────────────
    # Now start watching for
    # NEW files automatically!
    # ─────────────────────────

    # hire receptionist
    handler = FileSorterHandler(FILE_TYPES)

    # install CCTV camera
    observer = Observer()

    # tell camera: watch THIS folder, use THIS receptionist
    observer.schedule(handler, path=str(source_folder), recursive=False)

    # turn camera ON!
    observer.start()

    logger.info("------------------------------------")
    logger.info("Watching folder : TestSorter/")
    logger.info("Drop any file into TestSorter    ")
    logger.info("and it will be sorted instantly! ")
    logger.info("Press CTRL+C to stop watching.   ")
    logger.info("------------------------------------")

    # keep running forever
    try:
        while True:
            time.sleep(2)      # check every 2 seconds

    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()        # turn camera OFF!

    observer.join()            # wait for camera to fully stop
    logger.info("Watcher stopped! Goodbye!")