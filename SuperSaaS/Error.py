class Error(Exception):

    def __init__(self, message=None, status=None, errors=None):
        Exception.__init__(self, message)
        self.status = status
        self.errors = errors if errors is not None else []
