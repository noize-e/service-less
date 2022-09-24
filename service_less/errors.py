class LambdaError(Exception):
    pass


class InvalidRequestMethod(LambdaError):
    """ Raised when the request http method isnt whitelisted """
    def __init__(self, message: str="HTTP VERB is invalid", verb: str=None):
        self.code = 400
        message = f"{message} ({verb})" if verb else message
        super().__init__(message)


class InvalidRouterHandler(LambdaError):
    def __init__(self, message: str='Route handler function name is invalid'):
        self.code = 400
        super().__init__(message)
        