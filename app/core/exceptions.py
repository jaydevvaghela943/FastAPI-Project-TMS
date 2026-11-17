class AppException(Exception):
    def __init__(self, message:str):
        self.message = message
        super().__init__(message)

class UserNotFoundError(AppException):
    pass

class EmailAlreadyExistsError(AppException):
    pass

class InvalidTokenError(AppException):
    pass

class ProjectAlreadyExistsError(AppException):
    pass

class ProjectNotFoundError(AppException):
    pass

class TaskNotFoundError(AppException):
    pass