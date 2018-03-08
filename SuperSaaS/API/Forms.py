from .BaseApi import BaseApi
from ..Models.Form import Form


class Forms(BaseApi):
    def get(self, form_id):
        path = "/forms"
        query = {
            'id': self._validate_id(form_id)
        }
        res = self.client.get(path, query)
        return Form(res)

    def list(self, form_id, from_time=None):
        path = "/forms"
        query = {
            'form_id': self._validate_id(form_id)
        }
        if from_time:
            query['from_time'] = self._validate_datetime(from_time)
        res = self.client.get(path, query)
        return [Form(attributes) for attributes in res]
