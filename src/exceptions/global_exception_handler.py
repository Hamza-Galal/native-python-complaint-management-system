
from datetime import datetime, timezone

from exceptions.application_exception import ApplicationException


class GlobalExceptionHandler:

    @staticmethod
    def handle_exception(exception, path):

        if isinstance(exception, ApplicationException):
            status_code = exception.status_code
            error = exception.error
            message = exception.message

        else:
            status_code = 500
            error = "Internal Server Error"
            message = "An Unexpected Error Occurred"

        error_response = {
            "timestamp": datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            ),
            "status": status_code,
            "error": error,
            "message": message,
            "path": path
        }

        return status_code, error_response
