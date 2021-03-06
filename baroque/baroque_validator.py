class BaroqueValidator:
    def __init__(self, validation, validator, project):
        self.validation = validation
        self.validator = validator
        self.project = project
        if self.validation not in self.project.errors.keys():
            self.project.errors[validation] = []

    def validate(self):
        self.validator()
    
    def error(self, path, id, message):
        error_type = "requirement"
        self.project.add_errors(self.validation, error_type, path, id, message)

    def warn(self, path, id, message):
        error_type = "warning"
        self.project.add_errors(self.validation, error_type, path, id, message)
