from .BaseApi import BaseApi


class Hooks(BaseApi):
    """Manage webhooks (`/api/hooks`)."""

    def list(self):
        return self.client.get('/hooks')

    def create(self, target_url, event, parent_id):
        params = {
            'target_url': self._validate_present(target_url),
            'event': self._validate_present(event),
            'parent_id': self._validate_present(self._validate_id(parent_id))
        }
        return self.client.post('/hooks', params)

    def delete(self, hook_id, parent_id):
        query = {
            'id': self._validate_present(self._validate_id(hook_id)),
            'parent_id': self._validate_present(self._validate_id(parent_id))
        }
        return self.client.delete('/hooks', None, query)
