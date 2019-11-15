import os

CONFIG = os.path.join(os.path.expanduser("~"), ".baroque")
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BWFMETAEDIT = os.path.join(BASE_DIR, "tools", "bwfmetaedit.exe")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
