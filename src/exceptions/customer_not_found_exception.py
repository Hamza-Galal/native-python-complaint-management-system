from exceptions.application_exception import ApplicationException


class CustomerNotFoundException(ApplicationException):

    def __init__(self, message="Customer not found"):
        super().__init__(message, 404, "Not Found")
