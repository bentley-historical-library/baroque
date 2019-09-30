class BaroqueValidator:
    def __init__(self, validation, validator, project):
        self.validation = validation
        self.validator = validator
        self.project = project

    def validate(self):
        print("SYSTEM ACTIVITY: starting {}".format(self.validation))
        self.validator()
        print("SYSTEM ACTIVITY: ending {}".format(self.validation))
    
    def error(self, path, id, message):
        error_type = "requirement"
        self.project.add_errors(self.validation, error_type, path, id, message)

    def warn(self, path, id, message):
        error_type = "warning"
        self.project.add_errors(self.validation, error_type, path, id, message)
