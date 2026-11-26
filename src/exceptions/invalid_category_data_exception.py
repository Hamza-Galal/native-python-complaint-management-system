from exceptions.application_exception import ApplicationException


class InvalidCategoryDataException(ApplicationException):

    def __init__(self, message="Invalid category data"):
        super().__init__(message, 400, "Bad Request")