class ChecksumValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "checksum"
        validator = self.validate_checksums
        super().__init__(validation, validator, project)
    
    def validate_checksums(self):
        """ Validates checksums """
        pass
