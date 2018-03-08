from .BaseApi import BaseApi
from ..Models.Schedule import Schedule
from ..Models.Resource import Resource


class Schedules(BaseApi):

    def list(self):
        path = "/schedules"
        res = self.client.get(path)
        return [Schedule(attributes) for attributes in res]

    def resources(self, schedule_id):
        query = {
            'schedule_id': self._validate_id(schedule_id)
        }
        path = "/resources"
        res = self.client.get(path, query)
        return [Resource(attributes) for attributes in res]
