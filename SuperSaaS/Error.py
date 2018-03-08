class Error(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)