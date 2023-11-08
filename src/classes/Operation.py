from classes.Logger import Logger


class ValidationException(Exception):
    def __init__(self):
        super().__init__("The data passed to the operation is invalid.")


class Operation:
    """An operation in the pipe"""

    name: str

    def __init__(self, name: str):
        self.name = name

    def validate(self, data) -> bool:
        """Validate the data passed to the operation"""
        pass

    def execute(self, data, logger: Logger):
        """Execute the operation"""
        pass

    def save_data(self, data, path: str):
        """Save the data returned by the execute method"""
        pass

    def invoke(self, data, logger: Logger, logs_directory: str):
        """Invoke the operation: check the validity of the passed data, execute the method and save the data"""
        if not self.validate(data):
            raise ValidationException

        data = self.execute(data, logger)
        self.save_data(data, f"{logs_directory}/{self.name}")
        return data

    def __eq__(self, op1, op2):
        """Check whether or not two operations are the same"""
        return op1.name == op2.name
