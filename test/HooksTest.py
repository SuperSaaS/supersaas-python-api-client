import json
from urllib.parse import urlparse, parse_qs
from SuperSaaS import Error
from .Helper import SupersaasTest


class HooksTest(SupersaasTest):

    def __path(self):
        return urlparse(self.client.last_request.full_url).path

    def test_list(self):
        self.assertIsNotNone(self.client.hooks.list())
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertEqual('/api/hooks.json', self.__path())

    def test_create(self):
        self.assertIsNotNone(
            self.client.hooks.create('https://www.example.com/hook', 'U', 12345))
        self.assertEqual('POST', self.client.last_request.get_method())
        self.assertEqual('/api/hooks.json', self.__path())
        self.assertEqual(
            {'target_url': 'https://www.example.com/hook', 'event': 'U', 'parent_id': 12345},
            json.loads(self.client.last_request.data))

    def test_create_requires_params(self):
        with self.assertRaises(Error):
            self.client.hooks.create('', 'U', 12345)

    def test_delete(self):
        self.assertIsNotNone(self.client.hooks.delete(789, 12345))
        self.assertEqual('DELETE', self.client.last_request.get_method())
        self.assertEqual('/api/hooks.json', self.__path())
        self.assertEqual({'id': ['789'], 'parent_id': ['12345']},
                         parse_qs(urlparse(self.client.last_request.full_url).query))
        self.assertIsNone(self.client.last_request.data)
