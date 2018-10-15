class BaseModel(object):
    def __init__(self, attributes):
        for key in attributes:
            setattr(self, key, attributes[key])
