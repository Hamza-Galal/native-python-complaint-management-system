from exceptions.application_exception import ApplicationException

class ValidationException(ApplicationException):
    def __init__(self,message = "Validation Failed."):
        super().__init__(
            message,
            400,
            "Bad Request"
            )
        