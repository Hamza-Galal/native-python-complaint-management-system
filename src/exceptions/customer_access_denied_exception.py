from exceptions.application_exception import ApplicationException


class CustomerAccessDeniedException(ApplicationException):

    def __init__(self, message="You cannot access this customer"):
        super().__init__(message, 403, "Forbidden")
