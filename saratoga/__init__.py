import os

__version__ = "0.1.0"
basePath = os.path.abspath(os.path.dirname(__file__))

class APIError(Exception):
    code = 500

    def __init__(self, message, code=None):
        super(APIError, self).__init__(message)

class BadRequestParams(APIError):
    code = 400

class BadResponseParams(APIError):
    code = 500

class AuthenticationRequired(BadRequestParams):
    code = 401

class AuthenticationFailed(BadRequestParams):
    code = 403
