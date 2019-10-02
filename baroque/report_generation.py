import csv
import os

from datetime import datetime


def generate_reports(baroqueproject):
    data = []
    # Print out the number of errors and warnings for each validation.
    for validation, errors in baroqueproject.errors.items():
        num_requirements = len([error for error in errors if error["error_type"] == "requirement"])
        num_warnings = len([error for error in errors if error["error_type"] == "warning"])
        print("SYSTEM REPORT: {} validation has {} requirement error(s) and {} warning error(s)".format(validation, num_requirements, num_warnings))
        if (num_requirements + num_warnings) > 0:
            data.extend(errors)

    if data:
        # Create the csv file name with the following structure: directory-YYYYMMDD-HHMMSS.csv.
        date = datetime.now().strftime("%Y%m%d-%H%M%S")
        source = os.path.basename(baroqueproject.source_directory)
        csv_filename = source + "-" + date + ".csv"
        csv_filepath = os.path.join(baroqueproject.destination_directory, csv_filename)

        with open(csv_filepath, 'w', newline='') as csvfile:
            # Define and write header row values of csv file.
            fieldnames = ['validation', 'error_type', 'path', 'id', 'error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print("SYSTEM ACTIVITY: Detailed error report generated at {}".format(csv_filepath))
