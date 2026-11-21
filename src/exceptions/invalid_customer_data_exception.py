from exceptions.application_exception import ApplicationException


class InvalidCustomerDataException(ApplicationException):

    def __init__(self, message="Invalid customer data"):
        super().__init__(message, 400, "Bad Request")
