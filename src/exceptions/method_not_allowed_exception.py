from exceptions.application_exception import ApplicationException

class MethodNotAllowedException(ApplicationException):
    def __init__(self, message = " Http Method Not Allowed."):
        super().__init__(
            message,
            405,
            "Method Not Allowed"
            )