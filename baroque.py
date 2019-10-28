import argparse
import configparser
import os

from baroque.baroque_project import BaroqueProject
from baroque.checksum_validation import ChecksumValidator
from baroque.file_format_validation import FileFormatValidator
from baroque.mets_validation import MetsValidator
from baroque.report_generation import generate_reports
from baroque.structure_validation import StructureValidator
from baroque.wav_bext_chunk_validation import WavBextChunkValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to source directory")
    parser.add_argument("-d", "--destination", help="Path to destination for reports")
    parser.add_argument("-s", "--structure", action="store_true", help="Validate directory and file structure")
    parser.add_argument("-e", "--export", help="Path to metadata export")
    parser.add_argument("-m", "--mets", action="store_true", help="Validate METS")
    parser.add_argument("-w", "--wav", action="store_true", help="Validate WAV BEXT chunks")
    parser.add_argument("-f", "--files", action="store_true", help="Validate file formats")
    parser.add_argument("-c", "--checksums", action="store_true", help="Validate checksums")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini")
    if args.destination:
        project = BaroqueProject(args.source, args.destination, args.export)
    elif config["reports"]["path"]:
        project = BaroqueProject(args.source, config["reports"]["path"], args.export)
    else:
        if not os.path.isdir("reports"):
            os.mkdir("reports")
        project = BaroqueProject(args.source, "reports", args.export)
        
    if (args.structure or args.mets or args.wav) and not args.export:
        print("SYSTEM ERROR: metadata export [-e] is required for directory and file structure, METS validation and WAV BEXT chunks validations")
        sys.exit()

    if args.structure:
        StructureValidator(project).validate()
    if args.mets:
        MetsValidator(project).validate()
    if args.wav:
        WavBextChunkValidator(project).validate()
    if args.files:
        FileFormatValidator(project).validate()
    if args.checksums:
        ChecksumValidator(project).validate()

    generate_reports(project)


if __name__ == "__main__":
    print("SYSTEM ACTIVITY: baroque starting")
    main()
    print("SYSTEM ACTIVITY: baroque finished")
