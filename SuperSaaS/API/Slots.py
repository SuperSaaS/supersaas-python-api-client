from .BaseApi import BaseApi
from ..Models.Slot import Slot


class Slots(BaseApi):
    """Manage slots of capacity type schedules (`/api/slots`)."""

    ATTRIBUTES = ('start', 'finish', 'title', 'description', 'location',
                  'capacity', 'price', 'color')

    def list(self, schedule_id, start_time=None, finish=None, limit=None, offset=None):
        path = "/slots"
        query = {
            'schedule_id': self._validate_id(schedule_id),
            'start':
            self._validate_datetime(start_time) if start_time else None,
            'finish': self._validate_datetime(finish) if finish else None,
            'limit': self._validate_number(limit) if limit else None,
            'offset': self._validate_number(offset) if offset else None
        }
        res = self.client.get(path, query)
        return [Slot(attributes) for attributes in res]

    def get(self, schedule_id, slot_id):
        query = {'schedule_id': self._validate_id(schedule_id)}
        path = self.__slot_path(slot_id)
        res = self.client.get(path, query)
        return Slot(res)

    def create(self, schedule_id, attributes):
        path = "/slots"
        query = {'schedule_id': self._validate_id(schedule_id)}
        res = self.client.post(path, self.__params(attributes), query)
        return {'location': res}

    def update(self, schedule_id, slot_id, attributes):
        path = self.__slot_path(slot_id)
        query = {'schedule_id': self._validate_id(schedule_id)}
        return self.client.put(path, self.__params(attributes), query)

    def delete(self, schedule_id, slot_id):
        path = self.__slot_path(slot_id)
        query = {'schedule_id': self._validate_id(schedule_id)}
        return self.client.delete(path, None, query)

    def __slot_path(self, slot_id):
        return f"/slots/{self._validate_present(self._validate_id(slot_id))}"

    def __params(self, attributes):
        # Don't wrap attributes in 'slot' if they're already wrapped
        if isinstance(attributes, dict) and 'slot' in attributes:
            attributes = attributes['slot']
        attributes = attributes or {}
        slot = {}
        for key in self.ATTRIBUTES:
            value = attributes.get(key)
            if key in ('start', 'finish') and value is not None:
                value = self._validate_datetime(value)
            # capacity: '-' or None means unlimited, 0 means no places (server side)
            if value is not None:
                slot[key] = value
        return {'slot': slot}
