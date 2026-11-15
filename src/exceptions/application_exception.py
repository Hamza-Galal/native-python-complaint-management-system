class ApplicationException(Exception):
    def __init__(self, message , status_code,error):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.error = error