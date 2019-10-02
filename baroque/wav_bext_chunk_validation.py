from .baroque_validator import BaroqueValidator

class WavBextChunkValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "wav_bext_chunk"
        validator = self.validate_wav_bext_chunks
        super().__init__(validation, validator, project)

    def validate_wav_bext_chunks(self):
        """ Validates WAV BEXT chunks """
        pass
