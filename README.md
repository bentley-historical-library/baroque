# BAroQUe
BAroQUe: Bentley Audiovisual Quality control Utility

The **Bentley Audiovisual Quality control Utility (BAroQUe)** is a Python 3-based Command Line Interface (CLI) computer program primarily intended for in-house use. It performs Quality Control (QC)--with microservices for: 1) file naming and organization; 2) METS validation and verification; 3) WAV BEXT chunk validation and verification; 4) file format validation; and 5) checksum verification--for audio (and, eventually, video) digitized by vendors according to Bentley specifications.

## Contributors

- Dallas Pillen ([djpillen](https://github.com/djpillen))
- Hyeeyoung Kim ([hyeeyoungkim](https://github.com/hyeeyoungkim))
- Liz Gadelha ([lizgad](https://github.com/lizgad))
- Max Eckard ([eckardm](https://github.com/eckardm))
- Maryse Lundering-Timpano ([MaryseLT](https://github.com/MaryseLT))
- Matt Adair ([umadair](https://github.com/umadair))
- Melissa Hernández-Durán ([mhdezd](https://github.com/mhdezd))
- Tim Baron ([tlbaron](https://github.com/tlbaron))

## Requirements
- Requires Python 3.0 or higher.
- [dateparser](https://dateparser.readthedocs.io/en/latest/): To compare dates in metadata exports and METS XML
- [lxml](https://lxml.de/): To parse METS XML files
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/): To read xlsx files
- [tqdm](https://pypi.org/project/tqdm/): To make loops show a smart progress meter

## Installation
- Clone this repository to your computer
- `cd baroque`
- `pip install -r requirements.txt`

## Usage
```sh
usage: baroque.py [-h] [-d DESTINATION] [-s] [-m] [-w] [--all] SOURCE_DIR EXPORT_DIR
```

**Positional Arguments:**

| Argument | Description |
| --- | --- |
|SOURCE_DIR| Path to source directory |
|EXPORT_DIR|Path to metadata export file<br>|

**Actions:**

| Argument | Description |
| --- | --- |
|-s, --structure|Validate directory and file structure<br>For more information, see [Structure Validation documentation](docs/Structure_Validation.md).|
|-m, --mets|Validate METS<br>For more information, see [METS Validation documentation](docs/METS_Validation.md).|
|-w, --wav|Validate WAV BEXT chunks<br>For more information, see [BEXT Validation documentation](docs/BEXT_Validation.md).|
|--all|Run all validations|

**Optional Arguments:**

| Argument | Description |
| --- | --- |
|-h, --help|show the help message and exit|
|-d DESTINATION, --destination DESTINATION|Path to destination for reports|


BAroQUe's functionality is implemented in `baroque.py`, which is a command line script that takes as its input a minimum of 3 arguments:

**SOURCE_DIR**<br>The path to a source_directory that corresponds to either a shipment, a collection, or an item directory

**EXPORT_DIR**<br>The path to a metadata export (CSV or XLSX) corresponding to the shipment to validate against. BAroQUe expects this metadata export to contain at least the following column headers: "DigFile Calc", CollectionTitle", "ItemTitle", and "ItemDate".

**[-d, --destination]**<br>An _optional_ argument (`-d, --destination`) with a path to a destination directory where reports and logs will be stored. In the absence of this argument, BAroQUe checks a `.baroque` configuration file in the current user's home directory. Failing that, BAroQUe defaults to a `reports` directory in the BAroQUe installation's base directory.

**Actions**<br>The _optional_ validation action(s) to be run against the source directory (otherwise BAroQUe will just characterize the source directory as a shipment, collection or item)


### Command Examples ###

#### Validate directory and file structure

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -s/--structure
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -d/--destination /path/to/reports -s/--structure
```

#### Validate METS XML

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -m/--mets
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -d/--destination /path/to/reports -m/--mets
```

#### Validate WAV BEXT chunks

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -w/--wav
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -d/--destination /path/to/reports -w/--wav
```

#### Validate directory and file structure, METS XML and WAV BEXT chunks
This steps runs all validation checks described above.

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR --all
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_DIR -d/--destination /path/to/reports --all
```


### .baroque
A `.baroque` configuration file can be used to configure user-specific defaults, currently limited to configuring a default destination directory where reports will be saved. BAroQUe checks for a `.baroque` configuration file in the current user's home directory (e.g., `/home/username` or `C:\Users\username`) and will prompt the user to create the configuration file if it does not exist.

```ini
[defaults]
destination = path\to\default\reports\directory
```

## General Functionality

### BaroqueProject
Each of the quality control microservices uses a `BaroqueProject` object, which is defined in `baroque\baroque_project.py`. This object takes as its arguments a source directory, destination directory, and optionally a path to a metadata export. When it is first instantiated, the source directory is characterized as either a shipment, collection, or individual item. The directory is then parsed to identify all items present in the directory and to store the paths to items and filenames for all files found in each item directory. If a metadata export is given, various fields from the spreadsheet are parsed and also stored on the `BaroqueProject` object. Finally, the `BaroqueProject` object is used to store errors that are identified during each of Baroque's validation steps.

### BaroqueValidator
Each of the quality control microservices detailed above is a subclass of a base `BaroqueValidator` class, which is defined in `baroque/baroque_validator.py`. The `BaroqueValidator` base class takes as its arguments a name for the validation step, a function to use as a validator, and a `BaroqueProject` object. The `BaroqueValidator` base class implements a few shared functions, including `validate`, which runs the configured validation function, `error`, which adds a requirement error to the `BaroqueProject` object, and `warn`, which adds a warning error to the `BaroqueProject` object.

### Error reports
Error reports are generated within `baroque/report_generation.py`. This script checks the `BaroqueProject` object and, if any errors have been found, creates a CSV detailing the validation step in which the error was found, the error type (either a requirement or a warning error), the path to the item or file containing the error, the identifier for the item containing the error, and an error message. The CSV is saved to the destination directory supplied when running BAroQUe and used the filenaming convention `source_directory-timestamp.csv` to avoid duplicate filenames. An error report is not generated if no errors are found.

### System logs
As it is running, BAroQUe logs several system status updates to the command line. These include a report that BAroQUe is starting, the outcome of the source directory characterization, start and stop reports for each validation step that has been given, a high level report of number of requirement and warning errors found during each validation step, and a report that BAroQUe is finished.
