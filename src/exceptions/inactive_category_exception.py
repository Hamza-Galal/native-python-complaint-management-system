from exceptions.application_exception import ApplicationException


class InactiveCategoryException(ApplicationException):

    def __init__(self, message="Category is inactive"):
        super().__init__(message, 409, "Conflict")