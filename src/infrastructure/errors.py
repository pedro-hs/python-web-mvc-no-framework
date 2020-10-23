""" Error handlers """


class NotFound(Exception):
    """ 404 Not Found """

    def __init__(self, message):
        super().__init__(message)


class InternalServerError(Exception):
    """ 500 Internal Server Error """

    def __init__(self, message):
        super().__init__(message)
