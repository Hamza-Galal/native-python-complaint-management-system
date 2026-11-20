from exceptions.authentication_exception import AuthenticationException


class InvalidTokenException(AuthenticationException):

    def __init__(self):
        super().__init__("Invalid or expired token")