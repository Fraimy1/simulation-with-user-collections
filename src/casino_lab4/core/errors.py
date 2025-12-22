class CustomError(Exception):
    def __init__(self, message: str):
        self.message = message


class NotFoundError(CustomError): ...


class OutOfRangeError(CustomError): ...


class WrongTypeError(CustomError): ...


class StepZeroError(CustomError): ...
