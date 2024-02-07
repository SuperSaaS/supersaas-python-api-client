from .BaseApi import BaseApi
from ..Models.Form import Form
from ..Models.SuperForm import SuperForm


class Forms(BaseApi):

    def get(self, form_id):
        path = "/forms"
        query = {'id': self._validate_id(form_id)}
        res = self.client.get(path, query)
        return Form(res)

    def list(self, superform_id, from_time=None, user=None):
        path = "/forms"
        params = {'form_id': self._validate_id(superform_id)}
        if from_time:
            params['from_time'] = self._validate_datetime(from_time)
        if from_time:
            params['from'] = self._validate_datetime(from_time)
        if user or user == 0:
            params['user'] = self._validate_user(user)
        res = self.client.get(path, params)
        return [Form(attributes) for attributes in res]

    def forms(self):
        path = "/super_forms"
        res = self.client.get(path)
        return [SuperForm(attributes) for attributes in res]
