import csv
import datetime


def generate_reports(baroqueproject):
    # Create the csv file name with the following structure: directory-YYYYMMDD-HHMMSS.csv.
    date = (str(datetime.datetime.now())).split(".")[0].replace("-","").replace(":","").replace(" ","-")
    source = baroqueproject.source_directory
    csv_filename = source + "-" + date + ".csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        # Define and write header row values of csv file.
        fieldnames = ['validation', 'error_type', 'path', 'id', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Create and write rows to csv file.
        for validation in baroqueproject.errors.keys():
            for error in baroqueproject.errors[validation]:
                error["validation"] = validation
                writer.writerow(error)

    # Print out the number of errors and warnings for each validation.
    for validation in baroqueproject.errors.keys():
        num_requirements = 0
        num_warnings = 0

        for error in baroqueproject.errors[validation]:
            if error["error_type"] == "requirement":
                num_requirements += 1
            if error["error_type"] == "warning":
                num_warnings += 1

        print("SYSTEM REPORT: {} validation has {} requirement error(s) and {} warning error(s)".format(validation, num_requirements, num_warnings))
