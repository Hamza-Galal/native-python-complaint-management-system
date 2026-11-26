from exceptions.application_exception import ApplicationException


class DuplicateCategoryException(ApplicationException):

    def __init__(self, message="A category with this name already exists"):
        super().__init__(message, 409, "Conflict")