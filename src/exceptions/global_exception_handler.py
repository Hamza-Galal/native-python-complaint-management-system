from datetime import datetime
from exceptions.application_exception import ApplicationException

class GlobalExceptionHandler:
    @staticmethod
    def handle_exception(exception,path):
        if isinstance(exception,ApplicationException):
            status = exception.status_code
            error = exception.error
            message = exception.message
        else:
            status = 500
            error  = "Internal Server Error"
            message = "An Unexcpected Error Occured"

        error_response = {
            "timestamp": datetime.now().isoformat(timespec = "seconds"),
            "status": status,
            "error": error,
            "message": message,
            "path": path
        }

        return status , error_response