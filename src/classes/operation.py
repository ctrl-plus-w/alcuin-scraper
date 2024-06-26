"""Operation module"""
from dataclasses import dataclass

from src.classes.logger import Logger


class ValidationException(Exception):
    """Validation exception when the passed data isn't valid"""

    def __init__(self):
        super().__init__("The data passed to the operation is invalid.")


@dataclass
class Operation:
    """An operation in the pipe"""

    name: str

    def validate(self, _data) -> bool:
        """Validate the data passed to the operation"""
        return

    def execute(self, _data, _logger: Logger):
        """Execute the operation"""
        return 1

    def invoke(self, data, logger: Logger):
        """Invoke the operation: check the validity of the passed data, execute the method and save the data"""
        if not self.validate(data):
            raise ValidationException

        data = self.execute(data, logger)
        return data

    def __eq__(self, op):
        """Check whether or not two operations are the same"""
        return self.name == op.name
