import csv
import dateparser
import os
import subprocess
import io
from tqdm import tqdm

from .baroque_validator import BaroqueValidator
from .utils import sanitize_text


class WavBextChunkValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "wav_bext_chunk"
        validator = self.validate_wav_bext_chunks
        super().__init__(validation, validator, project)
    
    def get_paths_to_wavs(self, item):
        self.item_id = item["id"]
        self.path_to_item = item["path"]
        self.item_metadata = self.project.metadata["item_metadata"].get(self.item_id)
        paths_to_wavs = []
        path_to_item = item['path']
        wav_files = item['files']['wav']
        for wav_file in wav_files:
            paths_to_wavs.append(os.path.join(path_to_item, wav_file))
        
        return paths_to_wavs

    def get_bwfmetaedit_csv(self, path_to_wav):
        """
        Uses Windows 64-bit BWF MetaEdit CLI to get BEXT CSV:
        
        FileName,Description,Originator,OriginatorReference,OriginationDate,OriginationTime,TimeReference (translated),TimeReference,BextVersion,UMID,LoudnessValue,LoudnessRange,MaxTruePeakLevel,MaxMomentaryLoudness,MaxShortTermLoudness,CodingHistory,IARL,IART,ICMS,ICMT,ICOP,ICRD,IENG,IGNR,IKEY,IMED,INAM,IPRD,ISBJ,ISFT,ISRC,ISRF,ITCH
        R:\\BAroQUe\\2019012\\0648\\0648-SR-4\\0648-SR-4-1-2-am.wav,Paul Phillips (Tape No. 4),"US, MiU-H",MiU-H_0648-SR-4-1-am,2019-05-20,12:04:58,00:47:59.000,276384000,1,,,,,,,"A=ANALOGUE,M=mono,T=Studer A-810; 7.5 ips; open reel
A=PCM,F=96000,W=24,M=mono,T=Antelope Audio;Orion 32;A/D",,,,,,,"Schreibeis, Ryan",,,,,,,,,Reel-to-reel; 7 inch; Sony; None; Polyester"""

        bwfmetaedit_csv = subprocess.check_output(["./tools/bwfmetaedit.exe", "--out-core", path_to_wav], stderr=subprocess.STDOUT)

        return bwfmetaedit_csv

    def check_bext_metadatum_exists(self, path_to_wav, row, metadatum):
        if not row.get(metadatum):
            self.error(
                path_to_wav,
                self.item_id,
                metadatum + " does not exist"
            )

    def check_bext_metadatum_value_is(self, path_to_wav, row, metadatum, value):
        self.check_bext_metadatum_exists(path_to_wav, row, metadatum)
        if row.get(metadatum) and sanitize_text(row[metadatum]) != sanitize_text(value):
            self.error(
                path_to_wav,
                self.item_id,
                metadatum + " value of " + row[metadatum] + " in bext chunk does not equal " + value
            )

    def check_bext_metadatum_value_is_datetime(self, path_to_wav, row, metadatum):
        self.check_bext_metadatum_exists(path_to_wav, row, metadatum)
        if row.get(metadatum) and not dateparser.parse(row[metadatum]):
            self.error(
                path_to_wav,
                self.item_id,
                metadatum + " value of " + row[metadatum] + " is not datetime"
            )
    
    def check_coding_history(self, path_to_wav, row):
        # "A=ANALOGUE,M=mono,T=Studer A-810; 7.5 ips; open reel
        # A=PCM,F=96000,W=24,M=mono,T=Antelope Audio;Orion 32;A/D"
        self.check_bext_metadatum_exists(path_to_wav, row, "CodingHistory")
        if row.get("CodingHistory"):
            coding_histories = []
            for coding_history_line in row["CodingHistory"].splitlines():
                if coding_history_line:
                    coding_history = {}
                    subelements = coding_history_line.split(",")
                    for subelement in subelements:
                        subelement_tag = subelement.split("=")[0]
                        subelement_text = subelement.split("=")[1]
                        coding_history[subelement_tag] = subelement_text
                    coding_histories.append(coding_history)
        
            # BEXT chunk "Coding History" field may only use appropriate, comma-separated codes (A=, F=, B=, W=, M=, T=)
            acceptable_subelement_tags = [
                    "A", # Coding algorithm
                    "F", # Sampling frequency
                    "B", # Bit rate
                    "W", # Word length
                    "M", # Mode
                    "T" # Free ASCII text string
                ]
            for coding_history in coding_histories:
                for subelement_tag, _ in coding_history.items():
                    if subelement_tag not in acceptable_subelement_tags:
                        self.error(
                            path_to_wav,
                            self.item_id,
                            subelement_tag + " not in list of acceptable coding history subelement tags"
                        )
            # BEXT chunk "Coding History" field must have at least one A field
            coding_algorithms = 0
            for coding_history in coding_histories:
                for subelement_tag, _ in coding_history.items():
                    if subelement_tag == "A":
                        coding_algorithms += 1
            if coding_algorithms == 0:
                self.error(
                    path_to_wav,
                    self.item_id,
                    "no coding algorithm (a) field in coding history"
                )
            # BEXT chunk "Coding History" field A must be "ANALOG" or "PCM"
            for coding_history in coding_histories:
                for subelement_tag, subelement_text in coding_history.items():
                    if subelement_tag == "A" and subelement_text not in ["ANALOGUE", "PCM"]:
                        self.error(
                            path_to_wav,
                            self.item_id,
                            "coding algorithm (a) field value not ANALOGUE or PCM"
                        )
            # BEXT chunk "Coding History" field must have at least one F field
            sampling_frequencies = 0
            for coding_history in coding_histories:
                for subelement_tag, _ in coding_history.items():
                    if subelement_tag == "F":
                        sampling_frequencies += 1
            if sampling_frequencies == 0:
                self.error(
                    path_to_wav,
                    self.item_id,
                    "no sampling frequency (f) field in coding history"
                )
            # BEXT chunk "Coding History" field F must be 9600
            for coding_history in coding_histories:
                for subelement_tag, subelement_text in coding_history.items():
                    if subelement_tag == "F" and subelement_text != "96000":
                        self.error(
                            path_to_wav,
                            self.item_id,
                            "sampling frequency (f) field value not 96000"
                        )
            # BEXT chunk "Coding History" field must have at least one W field
            word_lengths = 0
            for coding_history in coding_histories:
                for subelement_tag, _ in coding_history.items():
                    if subelement_tag == "F":
                        word_lengths += 1
            if word_lengths == 0:
                self.error(
                    path_to_wav,
                    self.item_id,
                    "no word length (w) field in coding history"
                )
            # BEXT chunk "Coding History" field W must be 9600
            for coding_history in coding_histories:
                for subelement_tag, subelement_text in coding_history.items():
                    if subelement_tag == "W" and subelement_text != "24":
                        self.error(
                            path_to_wav,
                            self.item_id,
                            "word length (w) field value not 24"
                        )
            # BEXT chunk "Coding History" field must have at least one M field
            modes = 0
            for coding_history in coding_histories:
                for subelement_tag, _ in coding_history.items():
                    if subelement_tag == "M":
                        modes += 1
            if modes == 0:
                self.error(
                    path_to_wav,
                    self.item_id,
                    "no mode (m) field in coding history"
                )
            # BEXT chunk "Coding History" field must have at least one T field
            free_ascii_text_strings = 0
            for coding_history in coding_histories:
                for subelement_tag, _ in coding_history.items():
                    if subelement_tag == "T":
                        free_ascii_text_strings += 1
            if free_ascii_text_strings == 0:
                self.error(
                    path_to_wav,
                    self.item_id,
                    "no free ascii text string (t) field in coding history"
                )
            

    def validate_bwfmetaedit_csv(self, path_to_wav, bwfmetaedit_csv):
        with io.StringIO(bwfmetaedit_csv.decode("utf-8")) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self.item_metadata:
                    item_title = self.item_metadata.get("item_title")
                    self.check_bext_metadatum_value_is(path_to_wav, row, "Description", item_title)
                else:
                    self.warn(
                        path_to_wav,
                        self.item_id,
                        "item has no associated metadata in the metadata export spreadsheet to validate against wav bext chunk"
                    )
                    self.check_bext_metadatum_exists(path_to_wav, row, "Description")

                self.check_bext_metadatum_value_is(path_to_wav, row, "Originator", "US, MiU-H")
                originator_reference = "MiU-H_" + os.path.splitext(os.path.split(path_to_wav)[1])[0]
                self.check_bext_metadatum_value_is(path_to_wav, row, "OriginatorReference", originator_reference)

                self.check_bext_metadatum_value_is_datetime(path_to_wav, row, "OriginationDate")
                self.check_bext_metadatum_value_is_datetime(path_to_wav, row, "OriginationTime")

                self.check_bext_metadatum_exists(path_to_wav, row, "TimeReference")
                # self.check_bext_metadatum_exists(path_to_wav, row, "CodingHistory")

                self.check_coding_history(path_to_wav, row)


    def validate_wav_bext_chunks(self):
        """ 
        Validates WAV BEXT chunks """

        for item in tqdm(self.project.items, desc="WAV BEXT Chunk Validation"):
            paths_to_wavs = self.get_paths_to_wavs(item)
            for path_to_wav in paths_to_wavs: 
                bwfmetaedit_csv = self.get_bwfmetaedit_csv(path_to_wav)
                self.validate_bwfmetaedit_csv(path_to_wav, bwfmetaedit_csv)
