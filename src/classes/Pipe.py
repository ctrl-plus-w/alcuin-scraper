"""Pipe module"""
from src.classes.operation import Operation, ValidationException
from src.classes.logger import Logger


class Pipe:
    """A Pipe, running all the operations and pass the data from one operation to another one by one"""

    def __init__(self, logger: Logger, logs_directory: str):
        self.operations: list[Operation] = []

        self.data = None
        self.logger = logger
        self.logs_directory = logs_directory

    def add(self, operation: Operation):
        """Add an operation to the pipe"""
        self.operations.append(operation)

    def remove(self, operation: Operation):
        """Remove all the given operations in the pipe"""
        self.operations = filter(lambda o: o != operation, self.operations)

    def get_data(self):
        """Return the current pipe data"""
        return self.data

    def invoke(self, operation: Operation):
        """Invoke an operation from the pipe"""
        try:
            op_logger_name = f"{self.logger.name}/{operation.name}"
            op_logger = Logger(op_logger_name, self.logger.filename)

            return operation.invoke(self.data, op_logger, self.logs_directory)
        except ValidationException:
            self.logger.error(
                f"The data received for the operation {operation.name} is invalid."
            )
            return None

    def start(self, data=None):
        """Invoke all the pipe's operations"""
        self.data = data

        self.logger.info("Starting the pipe execution.")

        for operation in self.operations:
            self.logger.info(f"Executing the {operation.name} operation.")
            self.data = self.invoke(operation)
