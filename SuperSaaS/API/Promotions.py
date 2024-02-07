from .BaseApi import BaseApi
from ..Models.Promotion import Promotion


class Promotions(BaseApi):

    def list(self, limit=None, offset=None):
        path = '/promotions'
        params = {
            'limit':
            self._validate_number(limit) if limit is not None else None,
            'offset':
            self._validate_number(offset) if offset is not None else None
        }
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        res = self.client.get(path, params)
        return [Promotion(attributes) for attributes in res]

    def promotion(self, promotion_code):
        path = '/promotions'
        query = {'promotion_code': self._validate_promotion(promotion_code)}
        res = self.client.get(path, query)
        return [Promotion(attributes) for attributes in res]

    def duplicate_promotion_code(self, promotion_code, template_code):
        path = '/promotions'
        query = {
            'id': self._validate_promotion(promotion_code),
            'template_code': self._validate_promotion(template_code)
        }
        self.client.post(path, query)
