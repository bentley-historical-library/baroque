# BAroQUe
BAroQUe: Bentley Audiovisual Quality control Utility

The **Bentley Audiovisual Quality control Utility (BAroQUe)** is a Python 3-based Command Line Interface (CLI) executable primarily intended for in-house use. It performs Quality Control (QC)--with microservices to validate directory and file naming structure, METS XML and WAV BEXT chunks--for audio digitized by vendors according to Bentley specifications.

This README includes general installation and usage documentation for BAroQUe. For technical documentation intended to assist developers, check the project's [development documentation](docs/Developing.md).

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
usage: baroque.py [-h] [-d DESTINATION] [-s] [-m] [-w] [--all] SOURCE_DIR EXPORT_FILE
```

**Positional Arguments:**

| Argument | Description |
| --- | --- |
|SOURCE_DIR| Path to source directory |
|EXPORT_FILE|Path to metadata export file<br>|

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

**EXPORT_FILE**<br>The path to a metadata export (CSV or XLSX) corresponding to the shipment to validate against. BAroQUe expects this metadata export to contain at least the following column headers: "DigFile Calc", CollectionTitle", "ItemTitle", and "ItemDate".

**[-d, --destination]**<br>An _optional_ argument (`-d, --destination`) with a path to a destination directory where reports and logs will be stored. In the absence of this argument, BAroQUe checks a `.baroque` configuration file in the current user's home directory. Failing that, BAroQUe defaults to a `reports` directory in the BAroQUe installation's base directory.

**Actions**<br>The _optional_ validation action(s) to be run against the source directory (otherwise BAroQUe will just characterize the source directory as a shipment, collection or item)


### Command Examples ###

#### Validate directory and file structure

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -s/--structure
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -d/--destination /path/to/reports -s/--structure
```

#### Validate METS XML

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -m/--mets
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -d/--destination /path/to/reports -m/--mets
```

#### Validate WAV BEXT chunks

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -w/--wav
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -d/--destination /path/to/reports -w/--wav
```

#### Validate directory and file structure, METS XML and WAV BEXT chunks
This steps runs all validation checks described above.

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE --all
```

_or, with the optional destination argument..._

```sh
$ baroque.py SOURCE_DIR EXPORT_FILE -d/--destination /path/to/reports --all
```
