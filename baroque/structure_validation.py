import csv
import os
import sys

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


# structure_validation.py runs "validate_structure", which calls for "validate_directory" and "validate_file".
# "validate_directory" uses "parse_baroqueproject", "parse_metadata_export", "compare_ids", and "check_empty_directory".
# "validate_file" uses "check_empty_file".


def parse_baroqueproject(baroqueproject, level):
    ids = []
    paths = []

    for a in getattr(baroqueproject, level):
        ids.append(a["id"])
        paths.append(a["path"])

    return ids, paths


def parse_metadata_export(metadata_export, level):
    """
    This function parses collection IDs or item IDs from the "DigFile Calc" column in the metadata export file.
    The metadata export file can be either csv or xlsx.
    """
    if not os.path.exists(metadata_export):
        print("ERROR: metadata export does not exist")
        sys.exit()

    collection_ids = []
    items_ids = []

    # File type: csv
    if metadata_export.lower().endswith(".csv"):
        with open(metadata_export, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                item_id = row.get("DigFile Calc").strip()
                items_ids.append(item_id)

    # File type: xlsx
    elif metadata_export.lower().endswith(".xlsx"):
        workbook = load_workbook(metadata_export)
        sheet = workbook.active

        # Get the column letter for the "DigFile Calc" column
        target_col_letter = ""
        for col in sheet["1"]:
            if col.value == "DigFile Calc":
                target_col_letter = get_column_letter(col.column)
        # Set the range for rows (containing Item IDs) in the "DigFile Calc" column
        target_range = target_col_letter + "2:" + target_col_letter + str(sheet.max_row)

        for row in sheet[target_range]:
            for cell in row:
                item_id = cell.value.strip()
                items_ids.append(item_id)

    # File type: neither csv nor xlsx
    else:
        print("ERROR: metadata export is unexpected file type")
        sys.exit()

    # NOTE: Collection IDs are parsed from item IDs
    if level == "collections":
        for i in items_ids:
            collection_id = i.split("-")[0]
            if collection_id not in collection_ids:
                collection_ids.append(collection_id)
        return collection_ids

    elif level == "items":
        return items_ids


def compare_ids(set_a_ids, set_b_ids, level):
    diff_ids = list(set(set_a_ids) - set(set_b_ids)) + list(set(set_b_ids) - set(set_a_ids))
    if len(diff_ids) != 0:
        print("ERROR: following " + level[:-1] + " ids do not match:", diff_ids)


def check_empty_directory(directory_path):
    if len(os.listdir(directory_path)) == 0:
        print("ERROR: " + os.path.basename(directory_path) + " is empty directory")


def check_empty_file(file_path):
    for dirpath, dirnames, filenames in os.walk(file_path):
        for filename in filenames:
            if ".txt" not in filename:
                file_path = os.path.join(dirpath, filename)
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    print("ERROR: " + os.path.basename(file_path) + " is empty file")


def validate_directory(baroqueproject, metadata_export, level):
    """
    To validate a directory name, this function parses
    (1) IDs from a baroqueproject object (which is based on what the vendor returned) and
    (2) a metadata_export file (which is based on what BHL sent)
    create two ID lists, cross-compare the two ID lists, and print any ID that does not exists NOT in BOTH lists.
    It also checks for any empty directory.
    """
    process_ids, process_paths = parse_baroqueproject(baroqueproject, level)
    export_ids = parse_metadata_export(metadata_export, level)

    compare_ids(process_ids, export_ids, level)

    for path in process_paths:
        check_empty_directory(path)


def validate_file(baroqueproject):
    """
    This function validate (1) file names in an item-level directory and
    (2) the item-level directory itself (i.e., "is it well-formed?").
    It also checks any empty file (excepts for txt files) in an item-level directory.
    """
    for item in baroqueproject.items:
        audio_names = item["files"]["wav"] + item["files"]["mp3"] + item["files"]["md5"]
        unit_names = []
        name_formats = ["-am.wav.md5", "-pm.wav", "-pm.wav.md5", ".mp3", ".mp3.md5"]

        for wav_file in item["files"]["wav"]:
            if "am" in wav_file:
                unit_names.append(wav_file.replace("-am.wav", ""))

        # "Does all file names in this item folder starts with item ID?"
        for audio_name in audio_names:
            if not audio_name.startswith(item["id"]):
                print("ERROR: " + audio_name + " has invalid filename")

        # "Does each am-wav file in this item folder have respective pm-wav, mp3, md5 files?"
        for unit_name in unit_names:
            for name_format in name_formats:
                if not unit_name + name_format in audio_names:
                    print("ERROR: " + unit_name + "-am.wav" + " does not have " + name_format[1:] + " file")

        # "Does this item folder have 3 or more jpg files?"
        if len(item["files"]["jpg"]) == 0:
            print("ERROR: " + item["id"] + " does not include jpg file")
        elif len(item["files"]["jpg"]) < 3:
            print("ERROR: " + item["id"] + " includes less than 3 jpg file")

        # "Does this item folder have only 1 xml file?"
        if len(item["files"]["xml"]) == 0:
            print("ERROR: " + item["id"] + " does not include xml file")
        elif len(item["files"]["xml"]) > 1:
            print("ERROR: " + item["id"] + " includes more than 1 xml file")

        # "Does this item folder have either no or only 1 txt file?"
        if len(item["files"]["txt"]) > 1:
            print("ERROR: " + item["id"] + " includes more than 1 txt file")

        # "Does this item folder have any superfluous files?"
        if len(item["files"]["other"]) > 0:
            print("ERROR: " + item["id"] + " includes unexpected files:", item["files"]["other"])

        check_empty_file(item["path"])


def validate_structure(baroqueproject, metadata_export):
    """
    If the source directory is a shipment,
    this function runs "validate_directory" on collection/item-level and "validate_file" on item-level.
    If the source directory is a collection, it runs "validate_directory" and "validate_file" on item-level.
    If the source directory is an item, "validate_file" on item-level.
    """
    if baroqueproject.source_type == "shipment":
        if not os.path.exists(metadata_export):
            print("ERROR: metadata_export does not exist")
            sys.exit()
        else:
            levels = ["collections", "items"]
            for level in levels:
                validate_directory(baroqueproject, metadata_export, level)

    elif baroqueproject.source_type == "collection":
        if not os.path.exists(metadata_export):
            print("ERROR: metadata_export does not exist")
            sys.exit()
        else:
            level = "items"
            validate_directory(baroqueproject, metadata_export, level)

    validate_file(baroqueproject)
