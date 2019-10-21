import json
import os
import subprocess
from tqdm import tqdm

from .baroque_validator import BaroqueValidator

class WavBextChunkValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "wav_bext_chunk"
        validator = self.validate_wav_bext_chunks
        super().__init__(validation, validator, project)
    
    def get_paths_to_wavs(self, item):
        paths_to_wavs = []
        path_to_item = item['path']
        wav_files = item['files']['wav']
        for wav_file in wav_files:
            paths_to_wavs.append(os.path.join(path_to_item, wav_file))
        
        return paths_to_wavs

    def get_mediainfo_json(self, path_to_wav):
        """
        Uses Windows 64-bit MediaInfo CLI to return JSON:

        {'media': {'@ref': 'R:\\BAroQUe\\Transcription Discs '
                   'B2\\2018001\\86746\\86746-SR-10\\86746-SR-10-1-pm.wav',
           'track': [{'@type': 'General',
                      'AudioCount': '1',
                      'Description': 'WXYZ Michigan Radio Network, disc 3',
                      'Duration': '309.267',
                      'EncodedBy': 'Russak, Laura',
                      'Encoded_Date': '2018-08-23 14:51:51',
                      'Encoded_Library_Settings': 'A=ANALOGUE,M=mono,T=Technics '
                                                  'SL1210-MK2; 78 RPM; grooved '
                                                  'disc / '
                                                  'A=PCM,F=96000,W=24,M=mono,T=Antelope '
                                                  'Audio;Orion 32;A/D / '
                                                  'A=PCM,F=96000,W=24,M=mono,T=Steinberg;Wavelab '
                                                  '7; Normalize to 0dBFS / '
                                                  'A=PCM,F=96000,W=24,M=mono,T=Steinberg;Wavelab '
                                                  '7; Sonnox DeClicker',
                      'FileExtension': 'wav',
                      'FileSize': '89070016',
                      'File_Created_Date': 'UTC 2019-09-10 20:33:51.669',
                      'File_Created_Date_Local': '2019-09-10 16:33:51.669',
                      'File_Modified_Date': 'UTC 2018-08-23 18:52:07.910',
                      'File_Modified_Date_Local': '2018-08-23 14:52:07.910',
                      'Format': 'Wave',
                      'OriginalSourceForm': 'Grooved Disc; 12 inch; None',
                      'OverallBitRate': '2304029',
                      'OverallBitRate_Mode': 'CBR',
                      'Producer': 'US, MiU-H',
                      'StreamSize': '982',
                      'extra': {'Producer_Reference': 'MiU-H_86746-SR-10-1-pm',
                                'bext_Present': 'Yes'}},
                     {'@type': 'Audio',
                      'BitDepth': '24',
                      'BitRate': '2304000',
                      'BitRate_Mode': 'CBR',
                      'Channels': '1',
                      'CodecID': '1',
                      'Delay': '0.000000000',
                      'Delay_Source': 'Container (bext)',
                      'Duration': '309.267',
                      'Format': 'PCM',
                      'Format_Settings_Endianness': 'Little',
                      'Format_Settings_Sign': 'Signed',
                      'SamplingCount': '29689632',
                      'SamplingRate': '96000',
                      'StreamSize': '89069034',
                      'StreamSize_Proportion': '0.99999'}]}}"""

        output = subprocess.check_output(["./tools/MediaInfo.exe", path_to_wav, "--Output=JSON"])
        mediainfo_json = json.loads(output)
        
        return mediainfo_json
    
    def validate_wav_bext_chunks(self):
        """ 
        Validates WAV BEXT chunks """

        for item in tqdm(self.project.items):
            paths_to_wavs = self.get_paths_to_wavs(item)
            for path_to_wav in paths_to_wavs: 
                mediainfo_json = self.get_mediainfo_json(path_to_wav)
