import argparse

from baroque.baroque_project import BaroqueProject
from baroque.checksum_validation import validate_checksums
from baroque.file_format_validation import validate_file_formats
from baroque.mets_validation import validate_mets
from baroque.report_generation import generate_reports
from baroque.structure_validation import validate_structure
from baroque.wav_bext_chunk_validation import validate_wav_bext_chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to source directory")
    parser.add_argument("destination", help="Path to destination for reports")
    parser.add_argument("-s", "--structure", action="store_true", help="Validate directory and file structure")
    parser.add_argument("-e", "--export", help="Path to metadata export")
    parser.add_argument("-m", "--mets", action="store_true", help="Validate METS")
    parser.add_argument("-w", "--wav", action="store_true", help="Validate WAV BEXT chunks")
    parser.add_argument("-f", "--files", action="store_true", help="Validate file formats")
    parser.add_argument("-c", "--checksums", action="store_true", help="Validate checksums")
    args = parser.parse_args()

    project = BaroqueProject(args.source, args.destination)
    if args.structure:
        validation = "structure"
        print("SYSTEM ACTIVITY: {} {} validation".format("starting", validation))
        validate_structure(project, args.export)
        print("SYSTEM ACTIVITY: {} {} validation".format("ending", validation))
    if args.mets:
        validation = "mets"
        print("SYSTEM ACTIVITY: {} {} validation".format("starting", validation))
        validate_mets(project)
        print("SYSTEM ACTIVITY: {} {} validation".format("ending", validation))
    if args.wav:
        validation = "wav bext chunk"
        print("SYSTEM ACTIVITY: {} {} validation".format("starting", validation))
        validate_wav_bext_chunks(project)
        print("SYSTEM ACTIVITY: {} {} validation".format("ending", validation))
    if args.files:
        validation = "file format"
        print("SYSTEM ACTIVITY: {} {} validation".format("starting", validation))
        validate_file_formats(project)
        print("SYSTEM ACTIVITY: {} {} validation".format("ending", validation))
    if args.checksums:
        validation = "checksum"
        print("SYSTEM ACTIVITY: {} {} validation".format("starting", validation))
        validate_checksums(project)
        print("SYSTEM ACTIVITY: {} {} validation".format("ending", validation))

    generate_reports(project)


if __name__ == "__main__":
    print("SYSTEM ACTIVITY: baroque starting")
    main()
    print("SYSTEM ACTIVITY: baroque finished")
