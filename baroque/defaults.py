import os
import sys


# https://cx-freeze.readthedocs.io/en/latest/faq.html#data-files
def find_basedir():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        basedir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return basedir


CONFIG = os.path.join(os.path.expanduser("~"), ".baroque")
BASE_DIR = find_basedir()
BWFMETAEDIT = os.path.join(BASE_DIR, "tools", "bwfmetaedit.exe")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
