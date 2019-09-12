import csv
import os
import sys


def parse_baroqueproject(baroqueproject, level):
    ids = []
    paths = []

    for a in getattr(baroqueproject, level):
        ids.append(a["id"])
        paths.append(a["path"])

    return ids, paths


def parse_metadata_export(metadata_export, level):
    if not os.path.exists(metadata_export):
        print("ERROR: metadata export does not exist")
        sys.exit()

    collection_ids = []
    items_ids = []

    with open(metadata_export, "r", newline="") as f:
        reader = csv.DictReader(f)
        if level == "collections":
            for row in reader:
                collection_id = row.get("DigFile Calc").strip().split("-")[0]
                if collection_id not in collection_ids:
                    collection_ids.append(collection_id)

            return collection_ids

        elif level == "items":
            for row in reader:
                item_id = row.get("DigFile Calc").strip()
                items_ids.append(item_id)

            return items_ids


def compare_ids(set_a_ids, set_b_ids, level):
    diff_ids = list(set(set_a_ids) - set(set_b_ids)) + list(set(set_b_ids) - set(set_a_ids))
    if len(diff_ids) != 0:
        print("ERROR: following " + level[:-1] + " ids do not match:", diff_ids)


def check_empty_directory(directory_path):
    if len(os.listdir(directory_path)) == 0:
        print("ERROR: " + os.path.basename(directory_path) + " is empty")


def validate_directories(baroqueproject, metadata_export):
    levels = ["collections", "items"]

    for level in levels:
        process_ids, process_paths = parse_baroqueproject(baroqueproject, level)
        export_ids = parse_metadata_export(metadata_export, level)

        compare_ids(process_ids, export_ids, level)

        for path in process_paths:
            check_empty_directory(path)
