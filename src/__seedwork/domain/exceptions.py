class InvalidUuidException(Exception):
    def __init__(self, error="Id must be a valid UUID") -> None:
        super().__init__(error)


class ValidationException(Exception):
    def __init__(self, error="A validation error occurs") -> None:
        super().__init__(error)
