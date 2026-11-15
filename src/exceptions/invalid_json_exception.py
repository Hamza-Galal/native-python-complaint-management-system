from src.exceptions.application_exception import ApplicationException

class InvalidJsonException(ApplicationException):
    def __init__(self, message="Invalid Json Request Body."):
        super().__init__(
            message,
            400,
            "Bad Request"
            )