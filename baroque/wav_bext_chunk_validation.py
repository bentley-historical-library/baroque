import os
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
    
    def validate_wav_bext_chunks(self):
        """ 
        Validates WAV BEXT chunks """

        for item in tqdm(self.project.items):
            paths_to_wavs = self.get_paths_to_wavs(item)
