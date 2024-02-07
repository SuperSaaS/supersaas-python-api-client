from .BaseApi import BaseApi
from ..Models.Group import Group


class Groups(BaseApi):

    def list(self):
        path = '/groups'
        res = self.client.get(path)
        return [Group(attributes) for attributes in res]
