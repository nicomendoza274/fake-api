from core.schemas.error import Error


class GenericError(Exception):
    def __init__(self, foo: Error):
        self.error = foo
