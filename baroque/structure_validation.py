import os
import re
import sys
from tqdm import tqdm

from .baroque_validator import BaroqueValidator


# structure_validation.py runs "validate_structure", which calls for "validate_directory" and "validate_file"
# "validate_directory" uses "parse_baroqueproject", "parse_metadata_export", "compare_ids", and "check_empty_directory"
# "validate_file" uses "check_item_files" and "check_intellectual_groups"
# "check_item_files" uses "check_empty_file" and "check_intellectual_groups" uses "create_intellectual_groups"

class StructureValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "structure"
        validator = self.validate_structure
        super().__init__(validation, validator, project)


    def parse_baroqueproject(self, level):
        ids = []
        paths = []

        for a in getattr(self.project, level):
            ids.append(a["id"])
            paths.append(a["path"])

        return ids, paths


    def check_empty_directory(self, directory_path):
        if len(os.listdir(directory_path)) == 0:
            self.error(directory_path, os.path.basename(directory_path), "empty directory")


    def check_empty_file(self, file_path):
        for dirpath, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                if ".txt" not in filename:
                    file_path = os.path.join(dirpath, filename)
                    file_size = os.path.getsize(file_path)
                    if file_size == 0:
                        self.error(file_path, os.path.basename(file_path), "empty file")


    def validate_directory(self, level):
        """
        To validate a directory name, this function parses
        (1) IDs from a baroqueproject object (which is based on what the vendor returned) and
        (2) a metadata_export file (which is based on what BHL sent)
        create two ID lists, cross-compare the two ID lists, and print any ID that does not exists NOT in BOTH lists.
        It also checks for any empty directory.
        """
        process_ids, process_paths = self.parse_baroqueproject(level)
        export_ids = self.project.metadata["{}_ids".format(level)]

        diff_process_ids = list(set(process_ids) - set(export_ids))
        diff_export_ids = list(set(export_ids) - set(process_ids))

        # Report ids that do not exist in the metadata export as errors.
        if len(diff_process_ids) != 0:
            for id in diff_process_ids:
                for tuple_id, tuple_path in tuple(zip(process_ids, process_paths)):
                    if id == tuple_id:
                        path = tuple_path
                self.error(
                    path,
                    id,
                    level[:-1] + " id does not exist in metadata export"
                )

        # Report ids that do not exist in the directory as errors.
        if len(diff_export_ids) != 0:
            for id in diff_export_ids:
                self.error(
                    self.project.metadata_export,
                    id,
                    level[:-1] + " id does not exist in directory"
                )

        # Check for any empty directory.
        for path in process_paths:
            self.check_empty_directory(path)


    def check_item_files(self):
        """
        Check that the minimum number of required jpg, xml, and txt files are present for each item (e.g., 1234-SR-1).
        Check that each item does not have more than the maximum number of permissible files.
        Report out any "other" files and check whether any files are empty.
        """
        # Minimum number of files required.
        min_file_nums = {"jpg": 2, "xml": 1, "txt": 0}
        # Maximum number of files permissible.
        max_file_nums = {"xml": 1, "txt": 1}
        # List of "other" files that can be ignored.
        ignore_files = ["Thumbs.db", ".DS_Store", "Desktop DB", "Desktop DF"]
        # List of files that are checked.
        check_files = ["jpg", "xml", "txt", "other"]

        for item in tqdm(self.project.items, desc="Directory and File Structure Validation"):
            min_output = {}
            max_output = {}
            other_output = []
            name_output = []

            for file_type, files in item["files"].items():
                if file_type in check_files:
                    # For each item, output the file type and the number of files that are below the minimum requirements.
                    if file_type != "other":
                        if len(files) < min_file_nums.get(file_type):
                            min_output[file_type] = len(files)
                    # For each item, output the file type and the number of files that are above the maximum requirements.
                    if file_type in max_file_nums.keys():
                        if len(files) > max_file_nums.get(file_type):
                            max_output[file_type] = len(files)
                    # For each item, output the file type and the number of files that are identified as "other" files.
                    if file_type == "other":
                        if len(files) > 0:
                            other_output = files
                    # For each item, output the file names that do not start with the item id.
                    for file in files:
                        if not file.startswith(item["id"]):
                            name_output.append(file)

            if len(min_output.keys()) > 0:
                # For each file type, identify the minimum number of files missing and required.
                for type in min_output.keys():
                    missing = min_file_nums[type] - min_output[type]
                    required = min_file_nums[type]

                    # If there is only 1 jpg present, report as a warning.
                    if "jpg" in min_output.keys():
                        if min_output["jpg"] == 1:
                            self.warn(
                                item["path"],
                                item["id"],
                                "item missing {} of {} required '{}' file(s)".format(missing, required, type)
                        )
                    # For each item, for each file type, report missing required files as errors.
                    else:
                        self.error(
                            item["path"],
                            item["id"],
                            "item missing {} of {} required '{}' file(s)".format(missing, required, type)
                        )

            if len(max_output.keys()) > 0:
                # For each file type, identify the maximum number of files exceeded and required.
                for type in max_output.keys():
                    exceeding = max_output[type] - max_file_nums[type]
                    required = max_file_nums[type]

                    # For each item, for each file type, report excessive required files as errors.
                    self.error(
                        item["path"],
                        item["id"],
                         "item has {} extra '{}' file".format(exceeding, type)
                    )
            # For each item, report "other" files present as an error.
            if len(other_output) > 0:
                for file in other_output:
                    if file not in ignore_files:
                        self.error(
                            item["path"],
                            item["id"],
                            "item has unexpected file format: '{}'".format(file)
                        )
            # For each item, report file names that do not start with the item id as errors.
            if len(name_output) > 0:
                for file in name_output:
                    if file not in ignore_files:
                        self.error(
                            item["path"],
                            item["id"],
                            "file name does not start with item id: '{}'".format(file)
                        )

            self.check_empty_file(item["path"])


    def create_intellectual_groups(self):
        """
        Create intellectual groups of md5, mp3, and wav files, which make up a digital part.
        Return a dictionary with the following format:
            {
                item id (e.g., 85429-SR-1) :
                {
                    part id (e.g., 85429-SR-1-1) : [part files (e.g., 85429-SR-1-1-am.wav)]
                }
            }
        """
        part_file_types = ["md5", "mp3", "wav"]
        part_name_regex = re.compile(r"\d+\-SR-\d+(\-\d+){1,}")
        items = {}

        for item in self.project.items:
            for file_type, files in item["files"].items():
                if file_type in part_file_types:
                    for file in files:

                        # Isolate file names without extensions (e.g., "-am.wav").
                        name_match = part_name_regex.match(file)
                        if name_match:
                            name = name_match.group()

                            # Create dictionary of intellectual groups
                            if item["id"] not in items.keys():
                                items[item["id"]] = {}
                            if name not in items[item["id"]].keys():
                                items[item["id"]][name] = []
                            items[item["id"]][name].append(file)

        return items


    def check_intellectual_groups_numbers(self):
            """
            Make sure that intellectual groups are well-formed by checking that each part number is consecutively numbered.
            """
            items = self.create_intellectual_groups()

            for item in items.keys():
                # Find each item's path, which is needed for error reporting.
                for item_dict in self.project.items:
                    if item_dict["id"] == item:
                        path = item_dict["path"]

                # Check that each of the part numbers is consecutive
                part_ids = []
                consecutive = True

                for part_id in items[item].keys():
                    part_ids.append(part_id)

                part_ids.sort()

                # NOTE: This logic does not work when files have the following format: 1234-SR-1-1-1.
                for n in range(len(part_ids)):
                    if not part_ids[n].endswith(str(n + 1)):
                        consecutive = False

                if not consecutive:
                    # For each item, report digital parts that are not consecutively numbered as errors.
                    self.error(
                        path,
                        item,
                         "item has digital parts that are not consecutively numbered: {}".format(part_ids)
                    )


    def check_intellectual_groups_files(self):
        """
        Make sure that intellectual groups are well-formed by:
        (1) Checking that each part only has 6 files.
        (2) Checking that each part has exactly one of the 6 required file formats.
        Report any exceptions (e.g., more than 6 files, missing required files) as errors.
        """
        items = self.create_intellectual_groups()

        for item in items.keys():
            # Find each item's path, which is needed for error reporting.
            for item_dict in self.project.items:
                if item_dict["id"] == item:
                    path = item_dict["path"]

            for part in items[item]:
                count_formats = {"-am.wav": 0, "-am.wav.md5": 0, "-pm.wav": 0, "-pm.wav.md5": 0, ".mp3": 0, ".mp3.md5": 0, "other":[]}

                # If the digital part does not have exactly 6 files, identify extra or missing required file extensions in count_formats.
                # Also identify any files that do not end with the extensions listed in count_formats.
                if len(items[item][part]) != 6:
                    # Count the number of times each extension (e.g., -am.wav) occurs in the digital part.
                    for file in items[item][part]:
                        other = True
                        for format in count_formats.keys():
                            if file.endswith(format):
                                count_formats[format] += 1
                                other = False
                                break
                        if other == True:
                            count_formats["other"].append(file)

                    for format in count_formats.keys():
                        # For each digital part with more than 6 files, report any other file extensions as errors.
                        if format == "other":
                            if len(count_formats["other"]) > 0:
                                self.error(
                                    os.path.join(path, part),
                                    part,
                                    "digital part has {} total files, including {} other file(s): {}". format(len(items[item][part]), len(count_formats["other"]), count_formats["other"])
                                )
                        else:
                            # For each digital part with more than 6 files, report any extra file extensions as errors.
                            if count_formats[format] > 1:
                                self.error(
                                    os.path.join(path, part),
                                    part,
                                     "digital part has {} total files, including {} extra '{}' file(s)". format(len(items[item][part]), count_formats[format] - 1, format)
                                )
                            # For each digital part with more than 6 files, report any missing file extensions as errors.
                            if count_formats[format] < 1:
                                self.error(
                                    os.path.join(path, part),
                                    part,
                                    "digital part has {} total files and is missing 1 '{}' file". format(len(items[item][part]), format)
                                )

                # Check that a digital part with 6 files has one and only one of each of the required file extensions in count_formats.
                # Also identify any files that do not end with the extensions listed in count_formats.
                if len(items[item][part]) == 6:
                    # Count the number of times each extension (e.g., -am.wav) occurs in the digital part.
                    for file in items[item][part]:
                        other = True
                        for format in count_formats.keys():
                            if file.endswith(format):
                                count_formats[format] += 1
                                other = False
                                break
                        if other == True:
                            count_formats["other"].append(file)

                    for format in count_formats.keys():
                        # For each digital part with 6 files, report any other file extensions as errors.
                        if format == "other":
                            if len(count_formats["other"]) > 0:
                                self.error(
                                    os.path.join(path, part),
                                    part,
                                    "digital part has 6 files, but has {} other file(s): {}". format(len(items[item][part]), len(count_formats["other"]), count_formats["other"])
                                )
                        else:
                            # For each digital part with 6 files, report any extra file extensions as errors.
                            if count_formats[format] > 1:
                                extra = count_formats[format] - 1
                                self.error(
                                    os.path.join(path, part),
                                    part,
                                    "digital part has 6 total files, but has {} extra '{}' file(s)".format(extra, format)
                                )
                            # For each digital part with 6 files, report any missing file extensions as errors.
                            if count_formats[format] < 1:
                                self.error(
                                    os.path.join(path, part),
                                    part,
                                    "digital part has 6 total files, but is missing 1 '{}' file".format(format)
                                )

    def validate_file(self):
        self.check_item_files()
        self.check_intellectual_groups_numbers()
        self.check_intellectual_groups_files()


    def validate_structure(self):
        """
        If the source directory is a shipment,
        this function runs "validate_directory" on collection/item-level and "validate_file" on item-level.
        If the source directory is a collection, it runs "validate_directory" and "validate_file" on item-level.
        If the source directory is an item, "validate_file" on item-level.
        """
        if self.project.source_type == "shipment":
            levels = ["collections", "items"]
            for level in levels:
                self.validate_directory(level)

        elif self.project.source_type == "collection":
            level = "items"
            self.validate_directory(level)

        self.validate_file()
