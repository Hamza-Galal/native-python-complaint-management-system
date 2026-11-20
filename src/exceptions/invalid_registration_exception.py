
from exceptions.application_exception import ApplicationException


class InvalidRegistrationException(ApplicationException):

    def __init__(self, message="Invalid registration data"):
        super().__init__(
            message,
            400,
            "Invalid Registration"
        )
