from .BaseApi import BaseApi
from ..Models.User import User


class Users(BaseApi):
    def get(self, user_id=None):
        path = self.__user_path(user_id)
        res = self.client.get(path)
        return User(res)

    def list(self, form=None, limit=None, offset=None):
        path = self.__user_path()
        query = {
            'form': 'true' if form else None,
            'limit': self._validate_number(limit) if limit else None,
            'offset': self._validate_number(offset) if offset else None
        }
        res = self.client.get(path, query)
        return [User(attributes) for attributes in res]

    def create(self, attributes, user_id=None, webhook=None):
        path = self.__user_path(user_id)
        query = {'webhook': 'true' if webhook else None}
        params = {
            'user': {
                'name': self._validate_present(attributes.get('name','')),
                'email': attributes.get('email',None),
                'password': attributes.get('password',None),
                'full_name': attributes.get('full_name',None),
                'address': attributes.get('address',None),
                'mobile': attributes.get('mobile',None),
                'phone': attributes.get('phone',None),
                'country': attributes.get('country',None),
                'field_1': attributes.get('field_1',None),
                'field_2': attributes.get('field_2',None),
                'super_field': attributes.get('super_field',None),
                'credit': attributes.get('credit', None),
                'role': attributes.get('role',None)
            }
        }
        params['user'] = dict(filter(lambda item: item[1] is not None, params['user'].items()))
        res = self.client.post(path, params, query)
        return {'location': res}

    def update(self, user_id, attributes, webhook=None):
        path = self.__user_path(user_id)
        query = {'webhook': 'true' if webhook else None}
        params = {
            'webhook': attributes.get('webhook', None),
            'user': {
                'name': attributes.get('name',None),
                'email': attributes.get('email',None),
                'password': attributes.get('password',None),
                'full_name': attributes.get('full_name',None),
                'address': attributes.get('address',None),
                'mobile': attributes.get('mobile',None),
                'phone': attributes.get('phone',None),
                'country': attributes.get('country',None),
                'field_1': attributes.get('field_1',None),
                'field_2': attributes.get('field_2',None),
                'super_field': attributes.get('super_field',None),
                'credit': attributes.get('credit', None),
                'role': attributes.get('role',None)
            }
        }
        params['user'] = dict(filter(lambda item: item[1] is not None, params['user'].items()))
        return self.client.put(path, params, query)

    def delete(self, user_id):
        path = self.__user_path(self._validate_id(user_id))
        return self.client.delete(path)

    def __user_path(self, user_id=None):
        return "/users/{}".format(user_id) if user_id else "/users"
