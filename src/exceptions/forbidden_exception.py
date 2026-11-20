
from exceptions.application_exception import ApplicationException


class ForbiddenException(ApplicationException):

    def __init__(self, message="You do not have permission to perform this action"):
        super().__init__(
            message,
            403,
            "Forbidden"
        )
