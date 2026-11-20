
from exceptions.authentication_exception import AuthenticationException


class InvalidCredentialsException(AuthenticationException):

    def __init__(self):
        super().__init__("Invalid email or password")
