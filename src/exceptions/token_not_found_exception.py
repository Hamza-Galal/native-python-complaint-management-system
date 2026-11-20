
from exceptions.authentication_exception import AuthenticationException


class TokenNotFoundException(AuthenticationException):

    def __init__(self):
        super().__init__("Token not found")
