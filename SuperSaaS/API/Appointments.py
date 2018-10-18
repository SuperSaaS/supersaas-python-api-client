from .BaseApi import BaseApi
from ..Models.Appointment import Appointment
from ..Models.Slot import Slot


class Appointments(BaseApi):
    def agenda(self, schedule_id, user_id, from_time=None):
        path = "/agenda/{}".format(self._validate_id(schedule_id))
        query = {
            'user': self._validate_present(user_id),
            'from': self._validate_datetime(from_time) if from_time else None
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def agenda_slots(self, schedule_id, user_id, from_time=None):
        path = "/agenda/{}".format(self._validate_id(schedule_id))
        query = {
            'user': self._validate_present(user_id),
            'from': self._validate_datetime(from_time) if from_time else None,
            'slot': 'true'
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res, True)

    def available(self, schedule_id, from_time=None, length_minutes=None, resource=None, full=None, limit=None):
        path = "/free/{}".format(self._validate_id(schedule_id))
        query = {
            'length': self._validate_number(length_minutes) if length_minutes else None,
            'from': self._validate_datetime(from_time) if from_time else None,
            'resource': resource,
            'full': 'true' if full else None,
            'maxresults': self._validate_number(limit) if limit else None
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def list(self, schedule_id, form=None, start_time=None, limit=None):
        path = "/bookings"
        query = {
            'schedule_id': self._validate_id(schedule_id),
            'form': 'true' if form else None,
            'start': self._validate_datetime(start_time) if start_time else None,
            'limit': self._validate_number(limit) if limit else None
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def get(self, schedule_id, appointment_id=None):
        query = {schedule_id: self._validate_id(schedule_id)}
        path = "/bookings/{}".format(self._validate_id(appointment_id))
        res = self.client.get(path, query)
        return Appointment(res)

    def create(self, schedule_id, user_id, attributes, form=None, webhook=None):
        path = "/bookings"
        params = {
            'schedule_id': schedule_id,
            'webhook': webhook,
            'user_id': self._validate_id(user_id),
            'form': form,
            'booking': {
                'start': attributes.get('start', ''),
                'finish': attributes.get('finish', ''),
                'name': self._validate_present(attributes.get('name', '')),
                'email': attributes.get('email', ''),
                'full_name': attributes.get('full_name', ''),
                'address': attributes.get('address', ''),
                'mobile': attributes.get('mobile', ''),
                'phone': attributes.get('phone', ''),
                'country': attributes.get('country', ''),
                'field_1': attributes.get('field_1', ''),
                'field_2': attributes.get('field_2', ''),
                'field_1_r': attributes.get('field_1_r', ''),
                'field_2_r': attributes.get('field_2_r', ''),
                'super_field': attributes.get('super_field', ''),
                'resource_id': attributes.get('resource_id', ''),
                'slot_id': attributes.get('slot_id', '')
            }
        }
        res = self.client.post(path, params)
        return Appointment(res)

    def update(self, schedule_id, appointment_id, attributes, webhook=None):
        path = "/bookings/{}".format(self._validate_id(appointment_id))
        params = {
            'schedule_id': schedule_id,
            'webhook': webhook,
            'form': attributes.get('form', ''),
            'booking': {
                'start': attributes.get('start', ''),
                'finish': attributes.get('finish', ''),
                'name': self._validate_present(attributes.get('name', '')),
                'email': attributes.get('email', ''),
                'full_name': attributes.get('full_name', ''),
                'address': attributes.get('address', ''),
                'mobile': attributes.get('mobile', ''),
                'phone': attributes.get('phone', ''),
                'country': attributes.get('country', ''),
                'field_1': attributes.get('field_1', ''),
                'field_2': attributes.get('field_2', ''),
                'field_1_r': attributes.get('field_1_r', ''),
                'field_2_r': attributes.get('field_2_r', ''),
                'super_field': attributes.get('super_field', ''),
                'resource_id': attributes.get('resource_id', ''),
                'slot_id': attributes.get('slot_id', '')
            }
        }
        res = self.client.put(path, params)
        return Appointment(res)

    def delete(self, schedule_id, appointment_id):
        path = "/bookings/{}".format(self._validate_id(appointment_id))
        query = {
            'schedule_id': schedule_id
        }
        return self.client.delete(path, None, query)

    def changes(self, schedule_id, from_time=None):
        path = "/changes/{}".format(self._validate_id(schedule_id))
        query = {
            'from': self._validate_datetime(from_time) if from_time else None
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def changes_slots(self, schedule_id, from_time=None):
        path = "/changes/{}".format(self._validate_id(schedule_id))
        query = {
            'from': self._validate_datetime(from_time) if from_time else None,
            'slot': 'true'
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res, True)

    def __map_slots_or_bookings(self, obj, slot=False):
        if slot:
            return [Slot(attributes) for attributes in obj.get('slots', [])]
        elif isinstance(obj, list):
            return [Appointment(attributes) for attributes in obj]
        else:
            return [Appointment(attributes) for attributes in obj.get('bookings', [])]
