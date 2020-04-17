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
        return self.__map_slots_or_bookings(res)

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
        query = {'schedule_id': self._validate_id(schedule_id)}
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
                'start': attributes.get('start', None),
                'finish': attributes.get('finish', None),
                'name': attributes.get('name', None),
                'email': attributes.get('email', None),
                'full_name': attributes.get('full_name', None),
                'address': attributes.get('address', None),
                'mobile': attributes.get('mobile', None),
                'phone': attributes.get('phone', None),
                'country': attributes.get('country', None),
                'field_1': attributes.get('field_1', None),
                'field_2': attributes.get('field_2', None),
                'field_1_r': attributes.get('field_1_r', None),
                'field_2_r': attributes.get('field_2_r', None),
                'super_field': attributes.get('super_field', None),
                'resource_id': attributes.get('resource_id', None),
                'slot_id': attributes.get('slot_id', None),
                'description': attributes.get('description', None)
            }
        }
        params['booking'] = dict(filter(lambda item: item[1] is not None, params['booking'].items()))
        res = self.client.post(path, params)
        return {'location': res}

    def update(self, schedule_id, appointment_id, attributes, webhook=None):
        path = "/bookings/{}".format(self._validate_id(appointment_id))
        params = {
            'schedule_id': self._validate_id(schedule_id),
            'webhook': webhook,
            'form': attributes.get('form', None),
            'booking': {
                'start': attributes.get('start', None),
                'finish': attributes.get('finish', None),
                'name': attributes.get('name', ''),
                'email': attributes.get('email', None),
                'full_name': attributes.get('full_name', None),
                'address': attributes.get('address', None),
                'mobile': attributes.get('mobile', None),
                'phone': attributes.get('phone', None),
                'country': attributes.get('country', None),
                'field_1': attributes.get('field_1', None),
                'field_2': attributes.get('field_2', None),
                'field_1_r': attributes.get('field_1_r', None),
                'field_2_r': attributes.get('field_2_r', None),
                'super_field': attributes.get('super_field', None),
                'resource_id': attributes.get('resource_id', None),
                'slot_id': attributes.get('slot_id', None),
                'description': attributes.get('description', None)
            }
        }
        params['booking'] = dict(filter(lambda item: item[1] is not None, params['booking'].items()))
        res = self.client.put(path, params)
        return Appointment(res)

    def delete(self, schedule_id, appointment_id, webhook=None):
        params = {
            'webhook': webhook
        }
        path = '/bookings/{}'.format(self._validate_id(appointment_id))
        query = {
            'schedule_id': schedule_id
        }
        return self.client.delete(path, params, query)

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
        return self.__map_slots_or_bookings(res)

    def range(self, schedule_id, today=False, from_time=None, to=None, slot=False):
        path = "/range/{}".format(self._validate_id(schedule_id))
        query = {
                  'today': today if today else None,  
                  'from': self._validate_datetime(from_time) if from_time else None,
                  'to': self._validate_datetime(to) if to else None,
                  'slot': slot if slot else None 
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)


    def __map_slots_or_bookings(self, obj):
        if isinstance(obj, list):
            return [Appointment(attributes) for attributes in obj]
        elif 'slots' in obj:
            return [Slot(attributes) for attributes in obj.get('slots', [])]
        else:
            return [Appointment(attributes) for attributes in obj.get('bookings', [])]
