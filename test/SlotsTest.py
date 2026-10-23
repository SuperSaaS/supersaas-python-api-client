import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from SuperSaaS import Error
from .Helper import SupersaasTest


class SlotsTest(SupersaasTest):

    def __query(self):
        return parse_qs(urlparse(self.client.last_request.full_url).query)

    def __path(self):
        return urlparse(self.client.last_request.full_url).path

    def test_list(self):
        schedule_id = 12345
        self.assertIsNotNone(self.client.slots.list(schedule_id))
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertEqual('/api/slots.json', self.__path())
        self.assertEqual({'schedule_id': ['12345']}, self.__query())

    def test_list_all_params(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.slots.list(schedule_id, datetime(2030, 1, 31, 14, 30),
                                   "2030-02-01 00:00:00", 10, 5))
        query = self.__query()
        self.assertEqual(['2030-01-31 14:30:00'], query['start'])
        self.assertEqual(['2030-02-01 00:00:00'], query['finish'])
        self.assertEqual(['10'], query['limit'])
        self.assertEqual(['5'], query['offset'])

    def test_get(self):
        self.assertIsNotNone(self.client.slots.get(12345, 67890))
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertEqual('/api/slots/67890.json', self.__path())
        self.assertEqual({'schedule_id': ['12345']}, self.__query())

    def test_get_requires_slot_id(self):
        with self.assertRaises(Error):
            self.client.slots.get(12345, None)

    def test_create(self):
        self.assertIsNotNone(
            self.client.slots.create(12345, self.__slot_attributes()))
        self.assertEqual('POST', self.client.last_request.get_method())
        self.assertEqual('/api/slots.json', self.__path())
        self.assertEqual({'schedule_id': ['12345']}, self.__query())
        body = json.loads(self.client.last_request.data)
        self.assertEqual(
            {
                'slot': {
                    'start': '2030-01-31 10:00:00',
                    'finish': '2030-01-31 11:00:00',
                    'title': 'Yoga',
                    'capacity': '-',
                    'price': 12.5
                }
            }, body)

    def test_create_wrapped_attributes(self):
        self.client.slots.create(12345, {'slot': {'title': 'Yoga'}})
        self.assertEqual({'slot': {'title': 'Yoga'}},
                         json.loads(self.client.last_request.data))

    def test_create_invalid_datetime(self):
        with self.assertRaises(Error):
            self.client.slots.create(12345, {'start': 'tomorrow'})

    def test_update(self):
        self.assertIsNotNone(
            self.client.slots.update(12345, 67890, {'capacity': 0}))
        self.assertEqual('PUT', self.client.last_request.get_method())
        self.assertEqual('/api/slots/67890.json', self.__path())
        self.assertEqual({'schedule_id': ['12345']}, self.__query())
        self.assertEqual({'slot': {'capacity': 0}},
                         json.loads(self.client.last_request.data))

    def test_delete(self):
        self.assertIsNotNone(self.client.slots.delete(12345, 67890))
        self.assertEqual('DELETE', self.client.last_request.get_method())
        self.assertEqual('/api/slots/67890.json', self.__path())
        self.assertEqual({'schedule_id': ['12345']}, self.__query())
        self.assertIsNone(self.client.last_request.data)

    def __slot_attributes(self):
        return {
            'start': datetime(2030, 1, 31, 10, 0, 0),
            'finish': '2030-01-31 11:00:00',
            'title': 'Yoga',
            'capacity': '-',
            'price': 12.5,
            'unknown': 'ignored'
        }
