from .BaseApi import BaseApi
from ..Models.Appointment import Appointment
from ..Models.Slot import Slot


class Appointments(BaseApi):
    def agenda(self, schedule_id, user, from_time=None, slot=False):
        path = f"/agenda/{self._validate_id(schedule_id)}"
        query = {
            'user': self._validate_present(user),
            'from': self._validate_datetime(from_time) if from_time else None
        }
        if slot:
            query['slot'] = True
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)


    # LEGACY METHOD WILL BE REMOVED PLEASE USE AGENDA ABOVE
    def agenda_slots(self, schedule_id, user_id, from_time=None):
        path = f"/agenda/{self._validate_id(schedule_id)}"
        query = {
            'user': self._validate_present(user_id),
            'from': self._validate_datetime(from_time) if from_time else None,
            'slot': 'true'
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def available(self,
                  schedule_id,
                  from_time=None,
                  length_minutes=None,
                  resource=None,
                  full=None,
                  limit=None):
        path = f"/free/{self._validate_id(schedule_id)}"
        query = {
            'length':
            self._validate_number(length_minutes) if length_minutes else None,
            'from': self._validate_datetime(from_time) if from_time else None,
            'resource': resource,
            'full': 'true' if full else None,
            'maxresults': self._validate_number(limit) if limit else None
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def list(self, schedule_id, form=None, start_time=None, limit=None, finish=None):
        path = "/bookings"
        query = {
            'schedule_id': self._validate_id(schedule_id),
            'form': 'true' if form else None,
            'start':
            self._validate_datetime(start_time) if start_time else None,
            'limit': self._validate_number(limit) if limit else None,
            'finish':
                self._validate_datetime(finish) if finish else None
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def get(self, schedule_id, appointment_id=None):
        query = {'schedule_id': self._validate_id(schedule_id)}
        path = f"/bookings/{self._validate_id(appointment_id)}"
        res = self.client.get(path, query)
        return Appointment(res)

    def create(self, schedule_id, user_id, attributes,
               form=None,
               webhook=None):
        path = "/bookings"
        params = self.__create_update_params(schedule_id, attributes, form, webhook)
        if user_id:
            params['user_id'] = self._validate_id(user_id)
        params['booking'] = dict(
            filter(lambda item: item[1] is not None,
                   params['booking'].items()))
        res = self.client.post(path, params)
        return {'location': res}

    def __create_update_params(self, schedule_id, attributes, form, webhook):
        # Don't wrap attributes in 'booking' if they're already wrapped
        if attributes and isinstance(attributes, dict):
            if 'booking' in attributes:
                params = attributes
            else:
                params = {'booking': attributes}
        else:
            params = {'booking': {}}

        # Add optional parameters
        if form is not None:
            params['form'] = form
        if webhook is not None:
            params['webhook'] = webhook

        return params

    def update(self, schedule_id, appointment_id, attributes, form=None, webhook=None):
        """
        Update an existing appointment/booking
        """
        path = f"/bookings/{self._validate_id(appointment_id)}"
        params = self.__create_update_params(schedule_id, attributes, form, webhook)

        # Debug print
        print(f"Update params: {params}")
        print(f"Update path: {path}")

        # Ensure booking attributes are not None
        if params.get('booking') is None:
            params['booking'] = {}

        # Filter out None values from booking attributes
        params['booking'] = {k: v for k, v in params['booking'].items() if v is not None}

        try:
            res = self.client.put(path, params)
            return Appointment(res)
        except Exception as e:
            print(f"Update error: {str(e)}")
            print(f"Params sent: {params}")
            raise

    def delete(self, schedule_id, appointment_id, webhook=None):
        params = {'webhook': webhook}
        path = f'/bookings/{self._validate_id(appointment_id)}'
        query = {'schedule_id': schedule_id}
        return self.client.delete(path, params, query)

    def changes(self,
                schedule_id,
                from_time=None,
                to=None,
                slot=False,
                user=None,
                limit=None,
                offset=None):
        path = f"/changes/{self._validate_id(schedule_id)}"
        params = self.__build_param({}, from_time, to, slot, user, limit,
                                    offset)
        res = self.client.get(path, params)
        return self.__map_slots_or_bookings(res)

    # This is a legacy method, please use the changes method
    def changes_slots(self, schedule_id, from_time=None):
        path = f"/changes/{self._validate_id(schedule_id)}"
        query = {
            'from': self._validate_datetime(from_time) if from_time else None,
            'slot': 'true'
        }
        res = self.client.get(path, query)
        return self.__map_slots_or_bookings(res)

    def range(self,
              schedule_id,
              today=False,
              from_time=None,
              to=None,
              slot=False,
              user=None,
              resource_id=None,
              service_id=None,
              limit=None,
              offset=None):
        path = f"/range/{self._validate_id(schedule_id)}"
        params = {}
        params = self.__build_param(params, from_time, to, slot, user, limit,
                                    offset, resource_id, service_id)
        if today:
            params['today'] = True
        res = self.client.get(path, params)
        return self.__map_slots_or_bookings(res)

    def __create_update_params(self, schedule_id, attributes,
                               form=None,
                               webhook=None):
        params = {
            'schedule_id': self._validate_id(schedule_id),
            'booking': {
                'start': attributes.get('start', None),
                'finish': attributes.get('finish', None),
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
            }
        }
        if form:
            params['form'] = form
        if webhook:
            params['webhook'] = webhook
        return params

    def __map_slots_or_bookings(self, obj):
        if isinstance(obj, list):
            return [Appointment(attributes) for attributes in obj]
        if 'slots' in obj:
            return [Slot(attributes) for attributes in obj.get('slots', [])]
        return [
            Appointment(attributes)
            for attributes in obj.get('bookings', [])
        ]

    def __build_param(self,
                      params,
                      from_time,
                      to,
                      slot,
                      user,
                      limit,
                      offset,
                      resource_id=None,
                      service_id=None):
        if from_time:
            params['from'] = self._validate_datetime(from_time)
        if to:
            params['to'] = self._validate_datetime(to)
        if slot:
            params['slot'] = True
        if user or user == 0:
            params['user'] = self._validate_user(user)
        if limit:
            params['limit'] = self._validate_number(limit)
        if offset:
            params['offset'] = self._validate_number(offset)
        if resource_id is not None:
            params['resource_id'] = self._validate_id(resource_id)
        if service_id is not None:
            params['service_id'] = self._validate_id(service_id)

        return params
