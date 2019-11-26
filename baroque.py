import argparse

from baroque import defaults
from baroque.baroque_project import BaroqueProject
from baroque.config import get_config_setting
from baroque.mets_validation import MetsValidator
from baroque.report_generation import generate_reports
from baroque.structure_validation import StructureValidator
from baroque.wav_bext_chunk_validation import WavBextChunkValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to source directory")
    parser.add_argument("export", help="Path to metadata export")
    parser.add_argument("-d", "--destination", help="Path to destination for reports")

    action_args = parser.add_argument_group("actions")
    action_args.add_argument(
                            "-s", "--structure", dest="actions",
                            action="append_const", const="structure",
                            help="Validate directory and file structure"
                            )
    action_args.add_argument(
                            "-m", "--mets", dest="actions",
                            action="append_const", const="mets",
                            help="Validate METS"
                            )
    action_args.add_argument(
                            "-w", "--wav", dest="actions",
                            action="append_const", const="wav",
                            help="Validate WAV BEXT chunks"
                            )
    action_args.add_argument(
                            "--all", dest="actions", action="store_const",
                            const=["structure", "mets", "wav"],
                            help="Run all validations"
                            )
    args = parser.parse_args()

    if args.actions:
        actions = set(args.actions)
    else:
        parser.error("Please supply a validation action.")

    if args.destination:
        destination = args.destination
    else:
        destination = get_config_setting("destination", default=defaults.REPORTS_DIR)

    project = BaroqueProject(args.source, destination, args.export)
    if "structure" in actions:
        StructureValidator(project).validate()
    if "mets" in actions:
        MetsValidator(project).validate()
    if "wav" in actions:
        WavBextChunkValidator(project).validate()

    generate_reports(project)


if __name__ == "__main__":
    print("SYSTEM ACTIVITY: baroque starting")
    main()
    print("SYSTEM ACTIVITY: baroque finished")
