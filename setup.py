import inspect
import _strptime

from cx_Freeze import setup, Executable

# find _strptime to avoid dateparser packaging errors
strptime_datafile = inspect.getfile(_strptime)

executables = [Executable("baroque.py")]
build_exe_options = {
                    "packages": [
                                "argparse", "configparser", "csv", "dateparser",
                                "datetime", "io", "lxml", "openpyxl", "os", 
                                "subprocess", "sys", "tqdm", "unicodedata", "warnings"
                            ],
                    "include_files": [strptime_datafile, "tools/"]
                    }

setup(
    name="baroque",
    version="1.0",
    description="Baroque CLI",
    options={"build_exe": build_exe_options},
    executables=executables
)
