from exceptions.application_exception import ApplicationException


class CategoryNotFoundException(ApplicationException):

    def __init__(self, message="Category not found"):
        super().__init__(message, 404, "Not Found")
        