class FileFormatValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "file_format"
        validator = self.validate_file_formats
        super().__init__(validation, validator, project)

    def validate_file_formats(self):
        """ Validates file formats """
        pass
