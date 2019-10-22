import csv
import os
import subprocess
import io
from tqdm import tqdm

from .baroque_validator import BaroqueValidator

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

        bwfmetaedit_csv = subprocess.check_output(["./tools/bwfmetaedit.exe", "--out-core", path_to_wav])

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
        if row.get(metadatum) and row[metadatum] != value:
            self.error(
                path_to_wav,
                self.item_id,
                metadatum + " value of " + row[metadatum] + " does not equal " + value
            )

    def check_bext_metadatum_value_is_datetime(self, path_to_wav, row, metadatum):
        self.check_bext_metadatum_exists(path_to_wav, row, metadatum)
        if row.get(metadatum) and not dateparser.parse(row[metadatum]):
            self.error(
                path_to_wav,
                self.item_id,
                metadatum + " value of " + row[metadatum] + " is not datetime"
            )

    def validate_bwfmetaedit_csv(self, path_to_wav, bwfmetaedit_csv):
        with io.StringIO(bwfmetaedit_csv.decode()) as f:
            reader = csv.DictReader(f)
            for row in reader:
                item_title = self.item_metadata.get("item_title")
                self.check_bext_metadatum_value_is(path_to_wav, row, "Description", item_title)
                self.check_bext_metadatum_value_is(path_to_wav, row, "Originator", "US, MiU-H")
                originator_reference = "MiU-H_" + os.path.splitext(os.path.split(path_to_wav)[1])[0]
                self.check_bext_metadatum_value_is(path_to_wav, row, "OriginatorReference", originator_reference)
                self.check_bext_metadatum_value_is_datetime(path_to_wav, row, "OriginationDate")
                self.check_bext_metadatum_exists(path_to_wav, row, "TimeReference")
                self.check_bext_metadatum_value_is_datetime(path_to_wav, row, "OriginationTime")
                self.check_bext_metadatum_exists(path_to_wav, row, "CodingHistory")
    
    def validate_wav_bext_chunks(self):
        """ 
        Validates WAV BEXT chunks """

        for item in tqdm(self.project.items):
            paths_to_wavs = self.get_paths_to_wavs(item)
            for path_to_wav in paths_to_wavs: 
                bwfmetaedit_csv = self.get_bwfmetaedit_csv(path_to_wav)
                self.validate_bwfmetaedit_csv(path_to_wav, bwfmetaedit_csv)
