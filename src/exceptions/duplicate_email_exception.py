
from exceptions.application_exception import ApplicationException


class DuplicateEmailException(ApplicationException):

    def __init__(self):
        super().__init__(
            "Email already exists",
            409,
            "Duplicate Email"
        )
