from datetime import datetime
from urllib.parse import parse_qs, urlparse

from .Helper import SupersaasTest

class FormsTest(SupersaasTest):

    def test_get(self):
        super_form_id = 12345
        self.assertIsNotNone(self.client.forms.get(super_form_id))

    def test_list(self):
        form_id = 67890
        self.assertIsNotNone(self.client.forms.list(form_id, datetime.now()))

    def test_list_all(self):
        form_id = 67890
        user_id = 12345
        self.assertIsNotNone(
            self.client.forms.list(form_id, datetime.now(), user_id))

    def test_forms(self):
        self.assertIsNotNone(self.client.forms.forms())

    def test_list_query(self):
        self.client.forms.list(67890, '2030-01-31 14:30:00', 12345, 10, 20)
        query = parse_qs(urlparse(self.client.last_request.full_url).query)
        self.assertEqual(['67890'], query['form_id'])
        self.assertEqual(['2030-01-31 14:30:00'], query['from'])
        self.assertEqual(['12345'], query['user'])
        self.assertEqual(['10'], query['limit'])
        self.assertEqual(['20'], query['offset'])
