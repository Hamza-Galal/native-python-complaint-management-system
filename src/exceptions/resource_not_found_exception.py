from exceptions.application_exception import ApplicationException

class ResourceNotFoundException(ApplicationException):
    def __init__(self, message = "Resource Not Found."):
        super().__init__(
            message,
            404,
            "Not Found"
            )