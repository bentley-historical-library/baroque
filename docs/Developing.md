## Development Documentation
This file documents some of the more technical aspects of BAroQUe's functionality. It is intended to assist developers looking to modify the current funcationality. For usage documentation, check the project's [README](../README.md).

### BaroqueProject
Each of the quality control microservices uses a `BaroqueProject` object, which is defined in `baroque\baroque_project.py`. This object takes as its arguments a source directory, destination directory, and the path to a metadata export. When it is first instantiated, the source directory is characterized as either a shipment, collection, or individual item. The directory is then parsed to identify all items present in the directory and to store the paths to items and filenames for all files found in each item directory. Various fields from the metadata export are parsed and stored on the `BaroqueProject` object. Finally, the `BaroqueProject` object is used to store errors that are identified during each of BAroQUe's validation steps.

### BaroqueValidator
Each of the quality control microservices detailed in the [BAroQUe's README](../README.md) is a subclass of a base `BaroqueValidator` class, which is defined in `baroque/baroque_validator.py`. The `BaroqueValidator` base class takes as its arguments a name for the validation step, a function to use as a validator, and a `BaroqueProject` object. The `BaroqueValidator` base class implements a few shared functions, including `validate`, which runs the configured validation function, `error`, which adds a requirement error to the `BaroqueProject` object, and `warn`, which adds a warning error to the `BaroqueProject` object.

### Error reports
Error reports are generated within `baroque/report_generation.py`. This script checks the `BaroqueProject` object and, if any errors have been found, creates a CSV detailing the validation step in which the error was found, the error type (either a requirement or a warning error), the path to the item or file containing the error, the identifier for the item containing the error, and an error message. The CSV is saved to the destination directory supplied when running BAroQUe and uses the filenaming convention `source_directory-timestamp.csv` to avoid duplicate filenames. An error report is not generated if no errors are found.

### System logs
As it is running, BAroQUe logs several system status updates to the command line. These include a report that BAroQUe is starting, the outcome of the source directory characterization, a progress bar (using `tqdm`) for each validation action, a high level report of number of requirement and warning errors found during each validation step, and a report that BAroQUe is finished.

### Configuration file
A `.baroque` configuration file can be used to configure user-specific defaults, currently limited to configuring a default destination directory where reports will be saved. BAroQUe checks for a `.baroque` configuration file in the current user's home directory (e.g., `/home/username` or `C:\Users\username`) and will prompt the user to create the configuration file if it does not exist. The configuration file functionality is implemented in `baroque/config.py`. A sample configuration is provided below.

```ini
[defaults]
destination = path\to\default\reports\directory
```

### Building a release
BAroQUe uses the cx_Freeze Python module to create a `baroque.exe` file that can be shared with users without requiring them to install Python and BAroQUe's dependencies. The `setup.py` file in BAroQUe's root directory takes care of most of the work of ensuring that all Python packages and third party tools are included. If you are developing for BAroQUe and add any new required packages, add them to the `packages` array in `build_exe_options` within the `setup.py` file. Any tools added to the `tools/` directory will be included by default, but should be added according to the existing examples in `baroque/defaults.py` to ensure that they can be found by both the development version (`baroque.py`) and the executable (`baroque.exe`).

To build a new release, run the following command from within the BAroQUe root directory:

```
python setup.py build
```

This will create a `build/` directory with the BAroQUe root directory containing a subfolder (e.g., `exe.win32-3.7`) that contains a `baroque.exe` file, a copy of Python, and all of the modules, packages, data, and other files required to run `baroque.py`. Note that the version of Python and all dependencies will be the same as the versions installed in the environment in which the executable was created and that the executable can only be used on computers that share the same operating system as the machine on which the executable was created. The `baroque.exe` file functions exactly the same as `baroque.py`, e.g. to run all validation steps use the command `baroque.exe SOURCE_DIR EXPORT_FILE --all`. 