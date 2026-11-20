
from exceptions.application_exception import ApplicationException


class AuthenticationException(ApplicationException):

    def __init__(self, message="Authentication failed"):
        super().__init__(
            message,
            401,
            "Authentication Error"
        )
