from exceptions.application_exception import ApplicationException


class CustomerAlreadyInactiveException(ApplicationException):

    def __init__(self, message="Customer is already inactive"):
        super().__init__(message, 409, "Conflict")
