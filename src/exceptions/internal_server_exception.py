from exceptions.application_exception import ApplicationException

class InternalServerException(ApplicationException):
    def __init__(self, message="Internal Server Error."):
        super().__init__(
            message,
            500,
            "Internal Server Error"
            )